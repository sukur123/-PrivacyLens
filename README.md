# 🔍 PrivacyLens

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-green.svg)](https://developer.chrome.com/docs/extensions/)
[![Manifest V3](https://img.shields.io/badge/Manifest-V3-blue.svg)](https://developer.chrome.com/docs/extensions/mv3/)

**PrivacyLens** is a comprehensive open-source privacy analysis tool that helps users understand the privacy implications of websites they visit. It provides real-time privacy scoring and detailed security analysis through two main components:

## 🌐 Browser Extension
A Chrome/Brave compatible browser extension (Manifest V3) that:
- Analyzes cookies, third-party scripts, localStorage, sessionStorage, and iframes
- Provides real-time privacy scoring
- Shows privacy risks in an intuitive popup interface
- Uses color-coded visual indicators for easy understanding

## 🖥️ CLI Tool
A Python command-line tool that:
- Analyzes HTTP security headers (CSP, HSTS, X-Frame-Options, etc.)
- Checks SSL certificate validity and WHOIS information
- Provides colorful terminal reports
- Supports JSON output format

## 🚀 Quick Start

### Browser Extension
1. Navigate to `browser-extension/` directory
2. Load the extension in Chrome/Brave developer mode
3. Visit any website and click the PrivacyLens icon

### CLI Tool
```bash
cd cli-tool/
pip install -r requirements.txt
python -m privacylens check https://example.com
```

## 🎬 Demo

### Browser Extension Demo
```
🛡️ PrivacyLens Analysis for facebook.com

Privacy Score: 23/100 🔴

🔍 Privacy Issues Found:
🍪 Cookies: 47 total (23 tracking, 24 functional)
📜 Scripts: 12 tracking scripts detected
💾 Storage: 15 localStorage, 8 sessionStorage items
🖼️ iFrames: 3 third-party iframes detected
🖨️ Fingerprinting: Canvas fingerprinting detected
```

### CLI Tool Demo
```bash
$ privacylens check https://github.com

🔍 PrivacyLens Security Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 Website: https://github.com
📊 Privacy Score: 87/100 🟢

🔒 HTTP Security Analysis
✅ HTTPS Enabled
✅ HSTS Header Present
✅ Content Security Policy Configured
✅ X-Frame-Options: DENY

🔐 SSL Certificate Analysis
✅ Valid Certificate (expires in 197 days)
✅ Strong Encryption (TLS 1.3)

✅ Overall Assessment: Excellent privacy practices
```

## 📊 Privacy Scoring Algorithm

The privacy score starts at 100 and deductions are made based on:

### Browser Extension Analysis (-50 points total)
- **Cookies**: -1 per tracking cookie, -0.5 per functional cookie
- **Third-party scripts**: -2 per analytics/tracking script (Google Analytics, Facebook Pixel, etc.)
- **Local storage**: -1 per localStorage item, -0.5 per sessionStorage item
- **Iframes**: -3 per third-party iframe
- **Fingerprinting**: -5 for canvas fingerprinting, -3 for font detection

### CLI Analysis (-50 points total)
- **Missing HTTPS**: -15 points
- **No HSTS**: -5 points
- **Missing CSP**: -8 points
- **No X-Frame-Options**: -3 points
- **Weak referrer policy**: -4 points
- **Missing security headers**: -2 each
- **SSL issues**: -10 for expired/invalid certificates

## 🎨 Visual Design
- **Green (90-100)**: Excellent privacy protection
- **Yellow (70-89)**: Good with minor concerns
- **Orange (50-69)**: Moderate privacy risks
- **Red (0-49)**: Poor privacy protection

## 🛠️ Technology Stack
- **Browser Extension**: JavaScript (Manifest V3), HTML5, CSS3
- **CLI Tool**: Python 3.8+, requests, cryptography, colorama
- **Styling**: Modern UI with Google Material Design principles

## 📁 Project Structure
```
PrivacyLens/
├── browser-extension/          # Chrome/Brave extension
│   ├── manifest.json
│   ├── popup/
│   ├── background/
│   └── icons/
├── cli-tool/                   # Python CLI tool
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── docs/                       # Documentation
├── README.md
└── LICENSE
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Icon Suggestions
- **Main Logo**: Shield with magnifying glass
- **Privacy Score**: Traffic light system (🟢🟡🟠🔴)
- **Cookies**: 🍪 with warning overlay
- **Scripts**: ⚠️ for tracking, ℹ️ for functional
- **Storage**: 💾 with privacy indicator
- **HTTPS**: 🔒 (secure) / 🔓 (insecure)
- **Headers**: 🛡️ for security headers
