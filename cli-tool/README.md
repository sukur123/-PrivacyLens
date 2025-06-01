# PrivacyLens CLI Tool

A powerful command-line tool for analyzing website privacy and security.

## Installation

```bash
cd cli-tool/
pip install -r requirements.txt
```

## Usage

### Basic Analysis
```bash
python -m privacylens check https://example.com
```

### JSON Output
```bash
python -m privacylens check https://example.com --output json
```

### Save Report to File
```bash
python -m privacylens check https://example.com --save report.txt
```

### Batch Analysis
```bash
python -m privacylens batch https://site1.com https://site2.com https://site3.com
```

### Verbose Output
```bash
python -m privacylens check https://example.com --verbose
```

## Features

- **HTTP Security Headers Analysis**: Checks for HSTS, CSP, X-Frame-Options, and more
- **SSL Certificate Validation**: Verifies certificate validity and expiration
- **DNS Security**: Analyzes SPF, DMARC, and CAA records
- **Content Analysis**: Detects tracking scripts, analytics tools, and third-party resources
- **Privacy Score**: Calculates an overall privacy score (0-100)
- **Colored Output**: Beautiful terminal output with color coding
- **JSON Export**: Machine-readable output format
- **Batch Processing**: Analyze multiple websites at once

## Privacy Score Calculation

The privacy score starts at 100 and deductions are made for:

### HTTP Security (-40 points max)
- No HTTPS: -15 points
- Missing HSTS: -5 points
- Missing CSP: -8 points
- Missing X-Frame-Options: -3 points
- Insecure Referrer Policy: -4 points
- Missing security headers: -2-3 points each

### SSL Certificate (-20 points max)
- Invalid certificate: -15 points
- Expired certificate: -10 points
- Expires within 30 days: -5 points

### DNS Security (-15 points max)
- Missing SPF record: -3 points
- Missing DMARC record: -4 points
- Missing CAA records: -2 points

### Content Analysis (-25 points max)
- Tracking scripts: -2 points each (max 10)
- Analytics tools: -1 point each (max 5)
- Advertising networks: -3 points each (max 10)

## Example Output

```
🔍 PrivacyLens Security & Privacy Analysis Report
============================================================

🌐 Domain: example.com
🔗 URL: https://example.com
📅 Analysis Date: 2025-06-01 12:00:00 UTC

📊 PRIVACY SCORE
--------------------
Overall Score: 85/100 🟢 EXCELLENT
Progress: [█████████████████░░░] 85%

🔒 HTTP SECURITY HEADERS
------------------------------
HTTPS: ✅ Enabled

HSTS: ✅
CSP: ✅
X-Frame-Options: ✅
Referrer-Policy: ✅
X-Content-Type-Options: ✅
Permissions-Policy: ❌

🔐 SSL CERTIFICATE
--------------------
Status: ✅ VALID
Issuer: Let's Encrypt Authority X3
Valid Until: 2025-09-01 12:00:00
Days Until Expiry: 92

🌐 DNS SECURITY
---------------
SPF Record: ✅
DMARC Record: ✅
CAA Records: ❌

📄 CONTENT ANALYSIS
--------------------
Tracking Scripts: 2
Analytics Tools: 1
Ad Networks: 0
Social Widgets: 1

🎯 Detected Services:
  • Google Analytics (google-analytics.com)
  • Facebook SDK (facebook.net)

💡 RECOMMENDATIONS
--------------------
🟡 MEDIUM PRIORITY
  • Missing Permissions-Policy header
    → Add Permissions-Policy header to control browser features
  
  • Missing CAA records
    → Add CAA DNS records to control certificate issuance
```
