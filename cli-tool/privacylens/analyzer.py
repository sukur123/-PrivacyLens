"""
Privacy and Security Analyzer
Main analysis engine for PrivacyLens CLI tool
"""

import requests
import ssl
import socket
import whois
import dns.resolver
from urllib.parse import urlparse
from datetime import datetime, timezone
import re
from bs4 import BeautifulSoup
import json


class PrivacyAnalyzer:
    def __init__(self, timeout=10, verbose=False):
        self.timeout = timeout
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PrivacyLens/1.0.0 (Privacy Analysis Tool)'
        })
    
    def analyze(self, url):
        """Perform complete privacy and security analysis"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        if self.verbose:
            print(f"🔍 Starting analysis for {domain}")
        
        result = {
            'url': url,
            'domain': domain,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'analysis': {}
        }
        
        # Perform various analyses
        result['analysis']['http_security'] = self._analyze_http_security(url)
        result['analysis']['ssl_certificate'] = self._analyze_ssl_certificate(domain)
        result['analysis']['dns_security'] = self._analyze_dns_security(domain)
        result['analysis']['whois_info'] = self._analyze_whois(domain)
        result['analysis']['content_analysis'] = self._analyze_content(url)
        
        # Calculate privacy score
        result['privacy_score'] = self._calculate_privacy_score(result['analysis'])
        result['recommendations'] = self._generate_recommendations(result['analysis'])
        
        return result
    
    def _analyze_http_security(self, url):
        """Analyze HTTP security headers"""
        if self.verbose:
            print("  📡 Analyzing HTTP headers...")
        
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            headers = response.headers
            
            analysis = {
                'status_code': response.status_code,
                'final_url': response.url,
                'https_used': response.url.startswith('https://'),
                'headers': {}
            }
            
            # Security headers to check
            security_headers = {
                'strict-transport-security': 'HSTS',
                'content-security-policy': 'CSP', 
                'x-frame-options': 'X-Frame-Options',
                'x-content-type-options': 'X-Content-Type-Options',
                'referrer-policy': 'Referrer-Policy',
                'permissions-policy': 'Permissions-Policy',
                'x-xss-protection': 'X-XSS-Protection'
            }
            
            for header_name, display_name in security_headers.items():
                value = headers.get(header_name)
                analysis['headers'][display_name] = {
                    'present': value is not None,
                    'value': value,
                    'secure': self._evaluate_header_security(header_name, value)
                }
            
            # Check for insecure headers
            analysis['insecure_headers'] = self._check_insecure_headers(headers)
            
            return analysis
            
        except requests.RequestException as e:
            return {'error': str(e)}
    
    def _analyze_ssl_certificate(self, domain):
        """Analyze SSL certificate"""
        if self.verbose:
            print("  🔒 Analyzing SSL certificate...")
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse certificate dates
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    now = datetime.now()
                    
                    days_until_expiry = (not_after - now).days
                    
                    return {
                        'valid': True,
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'serial_number': cert['serialNumber'],
                        'version': cert['version'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'days_until_expiry': days_until_expiry,
                        'is_expired': days_until_expiry < 0,
                        'expires_soon': days_until_expiry < 30,
                        'san': cert.get('subjectAltName', [])
                    }
                    
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def _analyze_dns_security(self, domain):
        """Analyze DNS security features"""
        if self.verbose:
            print("  🌐 Analyzing DNS security...")
        
        analysis = {
            'caa_records': [],
            'mx_records': [],
            'spf_record': None,
            'dmarc_record': None,
            'dnssec': False
        }
        
        try:
            # Check CAA records
            try:
                caa_records = dns.resolver.resolve(domain, 'CAA')
                analysis['caa_records'] = [str(record) for record in caa_records]
            except:
                pass
            
            # Check MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                analysis['mx_records'] = [str(record) for record in mx_records]
            except:
                pass
            
            # Check SPF record
            try:
                txt_records = dns.resolver.resolve(domain, 'TXT')
                for record in txt_records:
                    record_str = str(record)
                    if record_str.startswith('"v=spf1'):
                        analysis['spf_record'] = record_str
                        break
            except:
                pass
            
            # Check DMARC record
            try:
                dmarc_records = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
                for record in dmarc_records:
                    record_str = str(record)
                    if 'v=DMARC1' in record_str:
                        analysis['dmarc_record'] = record_str
                        break
            except:
                pass
                
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def _analyze_whois(self, domain):
        """Analyze WHOIS information"""
        if self.verbose:
            print("  📋 Analyzing WHOIS data...")
        
        try:
            w = whois.whois(domain)
            
            # Calculate domain age
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            domain_age_days = None
            if creation_date:
                domain_age_days = (datetime.now() - creation_date).days
            
            return {
                'registrar': w.registrar,
                'creation_date': creation_date.isoformat() if creation_date else None,
                'expiration_date': w.expiration_date.isoformat() if w.expiration_date else None,
                'domain_age_days': domain_age_days,
                'name_servers': w.name_servers,
                'status': w.status,
                'privacy_protected': self._check_privacy_protection(w)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_content(self, url):
        """Analyze page content for privacy concerns"""
        if self.verbose:
            print("  📄 Analyzing page content...")
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            analysis = {
                'tracking_scripts': [],
                'social_widgets': [],
                'analytics_tools': [],
                'advertising_networks': [],
                'third_party_resources': []
            }
            
            # Find all script tags
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script.get('src')
                script_type = self._classify_script(src)
                
                if script_type['category']:
                    analysis[script_type['category']].append({
                        'url': src,
                        'service': script_type['service'],
                        'domain': self._extract_domain(src)
                    })
            
            # Find tracking pixels and beacons
            tracking_elements = soup.find_all(['img', 'iframe'], src=True)
            for element in tracking_elements:
                src = element.get('src')
                if self._is_tracking_resource(src):
                    analysis['third_party_resources'].append({
                        'type': element.name,
                        'url': src,
                        'domain': self._extract_domain(src)
                    })
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_privacy_score(self, analysis):
        """Calculate overall privacy score (0-100)"""
        score = 100
        
        # HTTP Security (40 points)
        http_security = analysis.get('http_security', {})
        if not http_security.get('https_used', False):
            score -= 15
        
        headers = http_security.get('headers', {})
        if not headers.get('HSTS', {}).get('present', False):
            score -= 5
        if not headers.get('CSP', {}).get('present', False):
            score -= 8
        if not headers.get('X-Frame-Options', {}).get('present', False):
            score -= 3
        if not headers.get('Referrer-Policy', {}).get('secure', False):
            score -= 4
        if not headers.get('X-Content-Type-Options', {}).get('present', False):
            score -= 2
        if not headers.get('Permissions-Policy', {}).get('present', False):
            score -= 3
        
        # SSL Certificate (20 points)
        ssl_cert = analysis.get('ssl_certificate', {})
        if not ssl_cert.get('valid', False):
            score -= 15
        elif ssl_cert.get('is_expired', False):
            score -= 10
        elif ssl_cert.get('expires_soon', False):
            score -= 5
        
        # DNS Security (15 points)
        dns_sec = analysis.get('dns_security', {})
        if not dns_sec.get('spf_record'):
            score -= 3
        if not dns_sec.get('dmarc_record'):
            score -= 4
        if not dns_sec.get('caa_records'):
            score -= 2
        
        # Content Analysis (25 points)
        content = analysis.get('content_analysis', {})
        tracking_count = len(content.get('tracking_scripts', []))
        analytics_count = len(content.get('analytics_tools', []))
        advertising_count = len(content.get('advertising_networks', []))
        
        score -= min(10, tracking_count * 2)
        score -= min(5, analytics_count * 1)
        score -= min(10, advertising_count * 3)
        
        return max(0, min(100, score))
    
    def _generate_recommendations(self, analysis):
        """Generate privacy improvement recommendations"""
        recommendations = []
        
        http_security = analysis.get('http_security', {})
        ssl_cert = analysis.get('ssl_certificate', {})
        dns_sec = analysis.get('dns_security', {})
        content = analysis.get('content_analysis', {})
        
        # HTTPS recommendations
        if not http_security.get('https_used', False):
            recommendations.append({
                'priority': 'high',
                'category': 'Security',
                'issue': 'No HTTPS encryption',
                'recommendation': 'Enable HTTPS with a valid SSL/TLS certificate'
            })
        
        # Security headers
        headers = http_security.get('headers', {})
        if not headers.get('HSTS', {}).get('present', False):
            recommendations.append({
                'priority': 'medium',
                'category': 'Security Headers',
                'issue': 'Missing HSTS header',
                'recommendation': 'Add Strict-Transport-Security header to enforce HTTPS'
            })
        
        if not headers.get('CSP', {}).get('present', False):
            recommendations.append({
                'priority': 'high',
                'category': 'Security Headers',
                'issue': 'Missing Content Security Policy',
                'recommendation': 'Implement CSP to prevent XSS and data injection attacks'
            })
        
        # SSL Certificate
        if ssl_cert.get('expires_soon', False):
            recommendations.append({
                'priority': 'medium',
                'category': 'SSL Certificate',
                'issue': 'SSL certificate expires soon',
                'recommendation': 'Renew SSL certificate before expiration'
            })
        
        # Privacy concerns
        tracking_scripts = content.get('tracking_scripts', [])
        if len(tracking_scripts) > 3:
            recommendations.append({
                'priority': 'medium',
                'category': 'Privacy',
                'issue': f'{len(tracking_scripts)} tracking scripts detected',
                'recommendation': 'Consider reducing third-party tracking scripts'
            })
        
        return recommendations
    
    def _evaluate_header_security(self, header_name, value):
        """Evaluate if a security header value is secure"""
        if not value:
            return False
        
        if header_name == 'strict-transport-security':
            return 'max-age=' in value.lower()
        elif header_name == 'content-security-policy':
            return len(value) > 10  # Basic check
        elif header_name == 'x-frame-options':
            return value.lower() in ['deny', 'sameorigin']
        elif header_name == 'referrer-policy':
            secure_policies = ['no-referrer', 'same-origin', 'strict-origin']
            return any(policy in value.lower() for policy in secure_policies)
        
        return True
    
    def _check_insecure_headers(self, headers):
        """Check for headers that reveal too much information"""
        insecure = []
        
        server = headers.get('server', '')
        if server and len(server) > 20:  # Detailed server info
            insecure.append('Detailed server information exposed')
        
        x_powered_by = headers.get('x-powered-by', '')
        if x_powered_by:
            insecure.append(f'Technology stack exposed: {x_powered_by}')
        
        return insecure
    
    def _check_privacy_protection(self, whois_data):
        """Check if domain privacy protection is enabled"""
        privacy_indicators = [
            'privacy', 'protection', 'proxy', 'whoisguard', 'domains by proxy'
        ]
        
        registrant = str(whois_data.registrant or '').lower()
        return any(indicator in registrant for indicator in privacy_indicators)
    
    def _classify_script(self, src):
        """Classify third-party scripts by service type"""
        services = {
            'google-analytics.com': {'category': 'analytics_tools', 'service': 'Google Analytics'},
            'googletagmanager.com': {'category': 'analytics_tools', 'service': 'Google Tag Manager'},
            'facebook.com': {'category': 'tracking_scripts', 'service': 'Facebook Pixel'},
            'facebook.net': {'category': 'tracking_scripts', 'service': 'Facebook SDK'},
            'doubleclick.net': {'category': 'advertising_networks', 'service': 'Google Ads'},
            'googlesyndication.com': {'category': 'advertising_networks', 'service': 'Google AdSense'},
            'hotjar.com': {'category': 'analytics_tools', 'service': 'Hotjar'},
            'mixpanel.com': {'category': 'analytics_tools', 'service': 'Mixpanel'},
            'twitter.com': {'category': 'social_widgets', 'service': 'Twitter'},
            'linkedin.com': {'category': 'social_widgets', 'service': 'LinkedIn'}
        }
        
        for domain, info in services.items():
            if domain in src:
                return info
        
        return {'category': None, 'service': 'Unknown'}
    
    def _is_tracking_resource(self, src):
        """Check if a resource is likely used for tracking"""
        tracking_patterns = [
            'analytics', 'tracking', 'pixel', 'beacon', 'metrics'
        ]
        return any(pattern in src.lower() for pattern in tracking_patterns)
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        try:
            return urlparse(url).netloc
        except:
            return 'unknown'
