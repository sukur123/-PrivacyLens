# 📖 PrivacyLens Usage Examples

## Browser Extension Examples

### Basic Usage
1. **Install Extension**
   - Open Chrome/Brave
   - Go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select `browser-extension` folder

2. **Analyze a Website**
   - Visit any website (e.g., `https://facebook.com`)
   - Click the PrivacyLens extension icon
   - View real-time privacy analysis

### Sample Extension Output
```
🛡️ PrivacyLens Analysis for facebook.com

Privacy Score: 23/100 🔴

🔍 Privacy Issues Found:
🍪 Cookies: 47 total (23 tracking, 24 functional)
📜 Scripts: 12 tracking scripts detected
   • Google Analytics
   • Facebook Pixel
   • DoubleClick Ads
💾 Storage: 15 localStorage items, 8 sessionStorage items
🖼️ iFrames: 3 third-party iframes
🖨️ Fingerprinting: Canvas fingerprinting detected

⚠️ Recommendations:
• Block tracking cookies in browser settings
• Use privacy-focused browser extensions
• Consider using Facebook Container
```

## CLI Tool Examples

### Basic Website Analysis
```bash
# Analyze a single website
python -m privacylens check https://github.com

# Verbose output
python -m privacylens check https://github.com --verbose

# JSON output
python -m privacylens check https://github.com --output json

# Save report to file
python -m privacylens check https://github.com --save github_privacy_report.txt
```

### Sample CLI Output (Text Format)
```
🔍 PrivacyLens Security Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 Website: https://github.com
🏷️  Domain: github.com
📅 Analyzed: 2025-06-01 10:30:45 UTC

📊 PRIVACY SCORE: 87/100 🟢

🔒 HTTP Security Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━
✅ HTTPS Enabled
✅ HSTS Header Present (max-age=31536000)
✅ Content Security Policy Configured
✅ X-Frame-Options: DENY
✅ X-Content-Type-Options: nosniff
✅ Referrer-Policy: strict-origin-when-cross-origin
⚠️  Permissions-Policy: Not configured

🔐 SSL Certificate Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Valid Certificate
✅ Certificate Chain Valid
✅ Expires: 2025-12-15 (197 days remaining)
✅ Strong Encryption (TLS 1.3)
✅ Perfect Forward Secrecy

🌍 DNS Security Analysis
━━━━━━━━━━━━━━━━━━━━━━━━
✅ DNSSEC Enabled
✅ DNS over HTTPS Supported
✅ No Suspicious DNS Records

📋 WHOIS Information
━━━━━━━━━━━━━━━━━━━━━
🏢 Organization: GitHub, Inc.
📅 Registration: 2007-10-09
📅 Expires: 2025-10-09
🌍 Country: United States

💡 Recommendations
━━━━━━━━━━━━━━━━━━━━━
• Consider implementing Permissions-Policy header
• Enable Certificate Transparency monitoring
• Regular security audits recommended

✅ Overall Assessment: Excellent privacy and security practices
```

### Sample CLI Output (JSON Format)
```json
{
  "url": "https://github.com",
  "domain": "github.com",
  "timestamp": "2025-06-01T10:30:45.123456+00:00",
  "privacy_score": 87,
  "analysis": {
    "http_security": {
      "is_https": true,
      "headers": {
        "hsts": {
          "present": true,
          "value": "max-age=31536000; includeSubDomains; preload",
          "secure": true
        },
        "csp": {
          "present": true,
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline'",
          "secure": true
        },
        "x_frame_options": {
          "present": true,
          "value": "DENY",
          "secure": true
        }
      }
    },
    "ssl_certificate": {
      "valid": true,
      "expires": "2025-12-15T23:59:59Z",
      "expires_soon": false,
      "issuer": "DigiCert Inc",
      "algorithm": "sha256WithRSAEncryption",
      "key_size": 2048
    },
    "dns_security": {
      "dnssec": true,
      "dns_over_https": true,
      "suspicious_records": false
    },
    "whois_info": {
      "organization": "GitHub, Inc.",
      "creation_date": "2007-10-09",
      "expiration_date": "2025-10-09",
      "country": "US"
    }
  },
  "recommendations": [
    "Consider implementing Permissions-Policy header",
    "Enable Certificate Transparency monitoring"
  ]
}
```

### Batch Analysis
```bash
# Analyze multiple websites
python -m privacylens batch https://github.com https://google.com https://facebook.com

# Save reports to directory
python -m privacylens batch https://github.com https://google.com --save-dir ./reports/

# JSON output for multiple sites
python -m privacylens batch https://github.com https://google.com --output json > batch_results.json
```

### Advanced Usage Examples

#### 1. Privacy Audit Script
```bash
#!/bin/bash
# audit_websites.sh - Audit multiple websites

websites=(
    "https://github.com"
    "https://stackoverflow.com"
    "https://reddit.com"
    "https://twitter.com"
    "https://facebook.com"
)

mkdir -p privacy_audit_$(date +%Y%m%d)
cd privacy_audit_$(date +%Y%m%d)

for site in "${websites[@]}"; do
    echo "Analyzing $site..."
    python -m privacylens check "$site" --output json --save "${site//https:\/\//}_report.json"
done

echo "Audit completed. Reports saved in $(pwd)"
```

#### 2. Continuous Monitoring
```bash
# Monitor a website daily
cat > monitor_site.sh << 'EOF'
#!/bin/bash
SITE="https://mywebsite.com"
DATE=$(date +%Y%m%d)
REPORT_FILE="privacy_monitor_${DATE}.json"

python -m privacylens check "$SITE" --output json --save "$REPORT_FILE"

# Check if score is below threshold
SCORE=$(jq '.privacy_score' "$REPORT_FILE")
if [ "$SCORE" -lt 70 ]; then
    echo "WARNING: Privacy score dropped to $SCORE for $SITE"
    # Send alert email, notification, etc.
fi
EOF

chmod +x monitor_site.sh

# Add to crontab for daily monitoring
# echo "0 9 * * * /path/to/monitor_site.sh" | crontab -
```

#### 3. Integration with CI/CD
```yaml
# .github/workflows/privacy-check.yml
name: Privacy Check
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  privacy-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install PrivacyLens
        run: |
          cd cli-tool
          pip install -r requirements.txt
          
      - name: Run Privacy Analysis
        run: |
          python -m privacylens check https://mywebsite.com --output json > privacy_report.json
          
      - name: Check Privacy Score
        run: |
          SCORE=$(jq '.privacy_score' privacy_report.json)
          echo "Privacy Score: $SCORE"
          if [ "$SCORE" -lt 80 ]; then
            echo "❌ Privacy score is below threshold (80)"
            exit 1
          else
            echo "✅ Privacy score meets requirements"
          fi
          
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: privacy-report
          path: privacy_report.json
```

## Real-World Use Cases

### 1. Security Team Audit
```bash
# Weekly security audit of company websites
python -m privacylens batch \
  https://company.com \
  https://app.company.com \
  https://blog.company.com \
  https://shop.company.com \
  --save-dir weekly_audit_$(date +%Y%m%d) \
  --output json

# Generate summary report
echo "Privacy Audit Summary - $(date)" > audit_summary.txt
for file in weekly_audit_*/*.json; do
    domain=$(jq -r '.domain' "$file")
    score=$(jq '.privacy_score' "$file")
    echo "$domain: $score/100" >> audit_summary.txt
done
```

### 2. Compliance Checking
```bash
# Check GDPR-related privacy features
python -m privacylens check https://eu-website.com --verbose | \
grep -E "(Cookie|GDPR|Privacy|Consent|Data)" > gdpr_compliance.txt
```

### 3. Competitive Analysis
```bash
# Compare privacy practices of competitors
competitors=(
    "https://competitor1.com"
    "https://competitor2.com" 
    "https://competitor3.com"
)

echo "Competitor Privacy Comparison" > comparison.txt
echo "=============================" >> comparison.txt

for comp in "${competitors[@]}"; do
    echo "Analyzing $comp..." >&2
    result=$(python -m privacylens check "$comp" --output json)
    score=$(echo "$result" | jq '.privacy_score')
    domain=$(echo "$result" | jq -r '.domain')
    echo "$domain: $score/100" >> comparison.txt
done

sort -nr -k2 comparison.txt
```

## Browser Extension Advanced Features

### Custom Privacy Rules
The extension allows users to configure custom privacy rules:

1. **Cookie Whitelist**: Allow specific cookies while blocking others
2. **Script Blocking**: Block specific tracking scripts
3. **Privacy Profiles**: Different privacy settings for different website categories

### Privacy Dashboard
The popup interface provides:
- Real-time privacy score updates
- Detailed breakdown of privacy issues
- Quick toggles for privacy features
- Historical privacy data for frequently visited sites

### Integration with Privacy Tools
The extension can work alongside:
- **uBlock Origin**: Enhanced ad and tracker blocking
- **Privacy Badger**: Intelligent tracker protection
- **ClearURLs**: URL parameter cleaning
- **Decentraleyes**: Local CDN emulation

## Troubleshooting

### Common CLI Issues
```bash
# SSL certificate errors
python -m privacylens check https://self-signed-site.com --timeout 30

# Network timeout issues
python -m privacylens check https://slow-site.com --timeout 60

# Permission errors
sudo python -m privacylens check https://restricted-site.com
```

### Browser Extension Debug
1. Open Chrome DevTools
2. Go to Console tab
3. Look for PrivacyLens log messages
4. Check for permission errors in Extensions tab

### Performance Optimization
- Use batch analysis for multiple sites
- Increase timeout for slow websites
- Enable caching for repeated analyses
- Use JSON output for programmatic processing
