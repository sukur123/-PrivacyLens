"""
Report Generator for PrivacyLens CLI
Generates formatted reports in text and JSON formats
"""

import json
from datetime import datetime
from colorama import init, Fore, Back, Style
import textwrap

# Initialize colorama
init(autoreset=True)


class Reporter:
    def __init__(self, output_format='text'):
        self.output_format = output_format
    
    def generate_report(self, analysis_result):
        """Generate report based on format"""
        if self.output_format == 'json':
            return self._generate_json_report(analysis_result)
        else:
            return self._generate_text_report(analysis_result)
    
    def _generate_text_report(self, result):
        """Generate colorful text report"""
        lines = []
        
        # Header
        lines.append(self._create_header(result))
        lines.append("")
        
        # Privacy Score
        lines.append(self._create_score_section(result))
        lines.append("")
        
        # Detailed Analysis Sections
        lines.append(self._create_http_security_section(result['analysis'].get('http_security', {})))
        lines.append("")
        
        lines.append(self._create_ssl_section(result['analysis'].get('ssl_certificate', {})))
        lines.append("")
        
        lines.append(self._create_dns_section(result['analysis'].get('dns_security', {})))
        lines.append("")
        
        lines.append(self._create_content_section(result['analysis'].get('content_analysis', {})))
        lines.append("")
        
        # Recommendations
        lines.append(self._create_recommendations_section(result.get('recommendations', [])))
        
        return "\n".join(lines)
    
    def _generate_json_report(self, result):
        """Generate JSON report"""
        return json.dumps(result, indent=2, default=str)
    
    def _create_header(self, result):
        """Create report header"""
        domain = result['domain']
        timestamp = datetime.fromisoformat(result['timestamp'].replace('Z', '+00:00'))
        
        header = f"""
{Fore.CYAN}{Style.BRIGHT}{'='*60}
🔍 PrivacyLens Security & Privacy Analysis Report
{'='*60}{Style.RESET_ALL}

🌐 Domain: {Fore.WHITE}{Style.BRIGHT}{domain}{Style.RESET_ALL}
🔗 URL: {result['url']}
📅 Analysis Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}
        """.strip()
        
        return header
    
    def _create_score_section(self, result):
        """Create privacy score section"""
        score = result.get('privacy_score', 0)
        
        # Color coding based on score
        if score >= 80:
            score_color = Fore.GREEN
            status = "🟢 EXCELLENT"
        elif score >= 60:
            score_color = Fore.YELLOW
            status = "🟡 GOOD"
        elif score >= 40:
            score_color = Fore.MAGENTA
            status = "🟠 MODERATE"
        else:
            score_color = Fore.RED
            status = "🔴 POOR"
        
        # Create progress bar
        filled = int(score / 5)  # 20 characters max
        empty = 20 - filled
        progress_bar = "█" * filled + "░" * empty
        
        section = f"""
{Fore.CYAN}{Style.BRIGHT}📊 PRIVACY SCORE{Style.RESET_ALL}
{'-' * 20}

Overall Score: {score_color}{Style.BRIGHT}{score}/100{Style.RESET_ALL} {status}

Progress: [{score_color}{progress_bar}{Style.RESET_ALL}] {score}%
        """.strip()
        
        return section
    
    def _create_http_security_section(self, http_security):
        """Create HTTP security headers section"""
        if 'error' in http_security:
            return f"""
{Fore.RED}{Style.BRIGHT}❌ HTTP SECURITY ANALYSIS FAILED{Style.RESET_ALL}
{'-' * 40}
Error: {http_security['error']}
            """.strip()
        
        lines = [
            f"{Fore.CYAN}{Style.BRIGHT}🔒 HTTP SECURITY HEADERS{Style.RESET_ALL}",
            "-" * 30
        ]
        
        # HTTPS status
        https_status = "✅ Enabled" if http_security.get('https_used', False) else "❌ Not Used"
        https_color = Fore.GREEN if http_security.get('https_used', False) else Fore.RED
        lines.append(f"HTTPS: {https_color}{https_status}{Style.RESET_ALL}")
        lines.append("")
        
        # Security headers
        headers = http_security.get('headers', {})
        for header_name, header_info in headers.items():
            if header_info['present']:
                status = "✅"
                color = Fore.GREEN
                if not header_info.get('secure', True):
                    status = "⚠️"
                    color = Fore.YELLOW
            else:
                status = "❌"
                color = Fore.RED
            
            lines.append(f"{header_name}: {color}{status}{Style.RESET_ALL}")
            
            if header_info['present'] and header_info['value']:
                # Truncate long values
                value = header_info['value']
                if len(value) > 50:
                    value = value[:50] + "..."
                lines.append(f"  Value: {Fore.LIGHTBLACK_EX}{value}{Style.RESET_ALL}")
        
        # Insecure headers
        insecure = http_security.get('insecure_headers', [])
        if insecure:
            lines.append("")
            lines.append(f"{Fore.YELLOW}⚠️ Security Concerns:")
            for concern in insecure:
                lines.append(f"  • {concern}")
        
        return "\n".join(lines)
    
    def _create_ssl_section(self, ssl_cert):
        """Create SSL certificate section"""
        lines = [
            f"{Fore.CYAN}{Style.BRIGHT}🔐 SSL CERTIFICATE{Style.RESET_ALL}",
            "-" * 20
        ]
        
        if 'error' in ssl_cert or not ssl_cert.get('valid', False):
            lines.append(f"{Fore.RED}❌ Invalid or No SSL Certificate{Style.RESET_ALL}")
            if 'error' in ssl_cert:
                lines.append(f"Error: {ssl_cert['error']}")
            return "\n".join(lines)
        
        # Certificate status
        if ssl_cert.get('is_expired', False):
            cert_status = f"{Fore.RED}❌ EXPIRED{Style.RESET_ALL}"
        elif ssl_cert.get('expires_soon', False):
            cert_status = f"{Fore.YELLOW}⚠️ EXPIRES SOON{Style.RESET_ALL}"
        else:
            cert_status = f"{Fore.GREEN}✅ VALID{Style.RESET_ALL}"
        
        lines.append(f"Status: {cert_status}")
        lines.append(f"Issuer: {ssl_cert.get('issuer', {}).get('organizationName', 'Unknown')}")
        lines.append(f"Valid Until: {ssl_cert.get('not_after', 'Unknown')}")
        
        days_left = ssl_cert.get('days_until_expiry', 0)
        if days_left >= 0:
            lines.append(f"Days Until Expiry: {days_left}")
        
        return "\n".join(lines)
    
    def _create_dns_section(self, dns_security):
        """Create DNS security section"""
        lines = [
            f"{Fore.CYAN}{Style.BRIGHT}🌐 DNS SECURITY{Style.RESET_ALL}",
            "-" * 15
        ]
        
        if 'error' in dns_security:
            lines.append(f"{Fore.YELLOW}⚠️ DNS analysis incomplete: {dns_security['error']}")
            return "\n".join(lines)
        
        # SPF Record
        spf_status = "✅" if dns_security.get('spf_record') else "❌"
        spf_color = Fore.GREEN if dns_security.get('spf_record') else Fore.RED
        lines.append(f"SPF Record: {spf_color}{spf_status}{Style.RESET_ALL}")
        
        # DMARC Record
        dmarc_status = "✅" if dns_security.get('dmarc_record') else "❌"
        dmarc_color = Fore.GREEN if dns_security.get('dmarc_record') else Fore.RED
        lines.append(f"DMARC Record: {dmarc_color}{dmarc_status}{Style.RESET_ALL}")
        
        # CAA Records
        caa_records = dns_security.get('caa_records', [])
        caa_status = "✅" if caa_records else "❌"
        caa_color = Fore.GREEN if caa_records else Fore.RED
        lines.append(f"CAA Records: {caa_color}{caa_status}{Style.RESET_ALL}")
        
        return "\n".join(lines)
    
    def _create_content_section(self, content_analysis):
        """Create content analysis section"""
        lines = [
            f"{Fore.CYAN}{Style.BRIGHT}📄 CONTENT ANALYSIS{Style.RESET_ALL}",
            "-" * 20
        ]
        
        if 'error' in content_analysis:
            lines.append(f"{Fore.YELLOW}⚠️ Content analysis failed: {content_analysis['error']}")
            return "\n".join(lines)
        
        # Tracking scripts
        tracking = content_analysis.get('tracking_scripts', [])
        tracking_color = Fore.RED if len(tracking) > 3 else Fore.YELLOW if len(tracking) > 0 else Fore.GREEN
        lines.append(f"Tracking Scripts: {tracking_color}{len(tracking)}{Style.RESET_ALL}")
        
        # Analytics tools
        analytics = content_analysis.get('analytics_tools', [])
        analytics_color = Fore.YELLOW if len(analytics) > 2 else Fore.GREEN
        lines.append(f"Analytics Tools: {analytics_color}{len(analytics)}{Style.RESET_ALL}")
        
        # Advertising networks
        advertising = content_analysis.get('advertising_networks', [])
        advertising_color = Fore.RED if len(advertising) > 0 else Fore.GREEN
        lines.append(f"Ad Networks: {advertising_color}{len(advertising)}{Style.RESET_ALL}")
        
        # Social widgets
        social = content_analysis.get('social_widgets', [])
        lines.append(f"Social Widgets: {Fore.CYAN}{len(social)}{Style.RESET_ALL}")
        
        # Show top tracking services
        all_trackers = tracking + analytics + advertising
        if all_trackers:
            lines.append("")
            lines.append(f"{Fore.YELLOW}🎯 Detected Services:")
            seen_services = set()
            for tracker in all_trackers[:5]:  # Show top 5
                service = tracker.get('service', 'Unknown')
                if service not in seen_services:
                    lines.append(f"  • {service} ({tracker.get('domain', 'unknown')})")
                    seen_services.add(service)
        
        return "\n".join(lines)
    
    def _create_recommendations_section(self, recommendations):
        """Create recommendations section"""
        if not recommendations:
            return f"""
{Fore.GREEN}{Style.BRIGHT}✅ RECOMMENDATIONS{Style.RESET_ALL}
{'-' * 20}
No specific recommendations - good privacy practices detected!
            """.strip()
        
        lines = [
            f"{Fore.CYAN}{Style.BRIGHT}💡 RECOMMENDATIONS{Style.RESET_ALL}",
            "-" * 20
        ]
        
        # Group by priority
        high_priority = [r for r in recommendations if r.get('priority') == 'high']
        medium_priority = [r for r in recommendations if r.get('priority') == 'medium']
        low_priority = [r for r in recommendations if r.get('priority') == 'low']
        
        for priority_group, title, color in [
            (high_priority, "🔴 HIGH PRIORITY", Fore.RED),
            (medium_priority, "🟡 MEDIUM PRIORITY", Fore.YELLOW),
            (low_priority, "🟢 LOW PRIORITY", Fore.GREEN)
        ]:
            if priority_group:
                lines.append(f"\n{color}{Style.BRIGHT}{title}{Style.RESET_ALL}")
                for rec in priority_group:
                    lines.append(f"  • {rec.get('issue', 'Unknown issue')}")
                    lines.append(f"    → {rec.get('recommendation', 'No recommendation')}")
                    lines.append("")
        
        return "\n".join(lines)
    
    def _wrap_text(self, text, width=70):
        """Wrap text to specified width"""
        return textwrap.fill(text, width=width, subsequent_indent="    ")
