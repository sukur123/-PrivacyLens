# 🛠️ PrivacyLens Development Guide

## Project Structure Overview

```
PrivacyLens/
├── 📁 browser-extension/     # Chrome/Brave Extension (Manifest V3)
│   ├── manifest.json         # Extension configuration
│   ├── 📁 background/        # Service worker and content scripts
│   │   ├── background.js     # Background service worker
│   │   └── content.js        # Content script for page analysis
│   ├── 📁 popup/            # Extension popup interface
│   │   ├── popup.html       # Popup HTML structure
│   │   ├── popup.css        # Popup styling
│   │   └── popup.js         # Popup functionality
│   └── 📁 icons/           # Extension icons
├── 📁 cli-tool/            # Python CLI Tool
│   ├── __main__.py         # CLI entry point
│   ├── requirements.txt    # Python dependencies
│   ├── 📁 src/            # Source code
│   │   ├── analyzer.py    # Core analysis engine
│   │   ├── reporter.py    # Report generation
│   │   └── utils.py       # Utility functions
│   └── 📁 tests/         # Unit tests
├── 📁 docs/               # Documentation
├── README.md             # Main project documentation
├── LICENSE              # MIT License
├── setup.sh            # Development setup script
└── ICONS.md           # Icon design guidelines
```

## Quick Start for Development

### 1. Environment Setup
```bash
# Clone and setup
git clone https://github.com/yourusername/PrivacyLens.git
cd PrivacyLens
chmod +x setup.sh
./setup.sh
```

### 2. CLI Tool Development
```bash
cd cli-tool
source venv/bin/activate  # Activate virtual environment

# Install in development mode
pip install -e .

# Run tests
python test_cli.py

# Example usage
python -m privacylens check https://example.com
python -m privacylens check https://example.com --output json
python -m privacylens batch https://google.com https://github.com
```

### 3. Browser Extension Development
```bash
cd browser-extension

# Load in Chrome for testing:
# 1. Open chrome://extensions/
# 2. Enable "Developer mode"
# 3. Click "Load unpacked"
# 4. Select the browser-extension folder
```

## Architecture Details

### Browser Extension Components

#### 1. Manifest V3 Configuration
- **Service Worker**: `background/background.js`
- **Content Scripts**: `background/content.js`
- **Popup Interface**: `popup/popup.html`
- **Permissions**: activeTab, storage, cookies, host permissions

#### 2. Privacy Analysis Features
- 🍪 **Cookie Analysis**: Tracks functional vs tracking cookies
- 📜 **Script Detection**: Identifies analytics and tracking scripts
- 💾 **Storage Analysis**: Monitors localStorage and sessionStorage
- 🖼️ **iFrame Detection**: Identifies third-party embeds
- 🖨️ **Fingerprinting Detection**: Canvas, WebGL, font detection

#### 3. Scoring Algorithm (Browser Extension)
```javascript
const calculateScore = (analysis) => {
    let score = 100;
    
    // Cookies penalty
    score -= analysis.cookies.tracking * 1;
    score -= analysis.cookies.functional * 0.5;
    
    // Scripts penalty
    score -= analysis.scripts.tracking * 2;
    score -= analysis.scripts.analytics * 1.5;
    
    // Storage penalty
    score -= analysis.storage.localStorage * 1;
    score -= analysis.storage.sessionStorage * 0.5;
    
    // iFrames penalty
    score -= analysis.iframes.thirdParty * 3;
    
    // Fingerprinting penalty
    if (analysis.fingerprinting.canvas) score -= 5;
    if (analysis.fingerprinting.webgl) score -= 3;
    if (analysis.fingerprinting.fonts) score -= 3;
    
    return Math.max(0, Math.round(score));
};
```

### CLI Tool Components

#### 1. Core Analysis Engine (`analyzer.py`)
- **HTTP Security Headers**: CSP, HSTS, X-Frame-Options, etc.
- **SSL Certificate Validation**: Expiry, chain verification
- **DNS Security**: DNSSEC, DNS over HTTPS
- **WHOIS Analysis**: Domain registration info
- **Content Analysis**: Meta tags, external resources

#### 2. Report Generation (`reporter.py`)
- **Text Output**: Colored terminal output with emojis
- **JSON Output**: Structured data for integration
- **HTML Output**: Web-friendly reports (future feature)

#### 3. Scoring Algorithm (CLI Tool)
```python
def calculate_privacy_score(analysis):
    score = 100
    
    # HTTPS check
    if not analysis['http_security']['is_https']:
        score -= 15
    
    # Security headers
    headers = analysis['http_security']['headers']
    if not headers.get('hsts'): score -= 5
    if not headers.get('csp'): score -= 8
    if not headers.get('x_frame_options'): score -= 3
    if not headers.get('referrer_policy'): score -= 4
    
    # SSL certificate
    ssl_info = analysis['ssl_certificate']
    if ssl_info['expires_soon']: score -= 5
    if ssl_info['self_signed']: score -= 10
    
    return max(0, score)
```

## Privacy Detection Logic

### Browser Extension Tracking Detection

#### Cookie Classification
```javascript
const trackingCookiePatterns = [
    /_ga/, /_gid/, /fbp/, /fbclid/, /_fbp/,  // Analytics
    /doubleclick/, /adsystem/, /googlesyndication/,  // Ads
    /__utm/, /campaign/, /affiliate/  // Marketing
];

const isTrackingCookie = (name) => {
    return trackingCookiePatterns.some(pattern => pattern.test(name));
};
```

#### Script Analysis
```javascript
const trackingScripts = [
    'google-analytics.com', 'googletagmanager.com',
    'facebook.net', 'connect.facebook.net',
    'doubleclick.net', 'googlesyndication.com',
    'hotjar.com', 'mixpanel.com', 'segment.com'
];

const analyzeScripts = () => {
    const scripts = document.querySelectorAll('script[src]');
    scripts.forEach(script => {
        const src = script.src;
        if (trackingScripts.some(domain => src.includes(domain))) {
            // Found tracking script
        }
    });
};
```

### CLI Tool Security Analysis

#### HTTP Headers Analysis
```python
SECURITY_HEADERS = {
    'strict-transport-security': 'hsts',
    'content-security-policy': 'csp',
    'x-frame-options': 'x_frame_options',
    'x-content-type-options': 'x_content_type_options',
    'referrer-policy': 'referrer_policy',
    'permissions-policy': 'permissions_policy'
}

def analyze_security_headers(headers):
    results = {}
    for header, key in SECURITY_HEADERS.items():
        results[key] = {
            'present': header in headers,
            'value': headers.get(header, ''),
            'secure': is_secure_value(header, headers.get(header, ''))
        }
    return results
```

## Testing Strategy

### Browser Extension Testing
1. **Manual Testing**: Load extension and visit various websites
2. **Console Logging**: Check browser console for analysis data
3. **Permission Testing**: Verify required permissions work
4. **Cross-browser Testing**: Test on Chrome, Brave, Edge

### CLI Tool Testing
1. **Unit Tests**: Test individual analysis functions
2. **Integration Tests**: Test complete analysis workflow
3. **Error Handling**: Test with invalid URLs and timeouts
4. **Output Validation**: Verify JSON and text output formats

## Contributing Guidelines

### Code Style
- **JavaScript**: Use ES6+ features, consistent indentation
- **Python**: Follow PEP 8, use type hints where appropriate
- **CSS**: Use consistent naming, mobile-responsive design

### Git Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-analysis`
3. Commit changes: `git commit -m "Add new privacy analysis feature"`
4. Push to branch: `git push origin feature/new-analysis`
5. Create Pull Request

### Adding New Analysis Features

#### Browser Extension
1. Add detection logic to `content.js`
2. Update scoring algorithm in `popup.js`
3. Add UI elements to `popup.html` and `popup.css`

#### CLI Tool
1. Add analysis method to `analyzer.py`
2. Update report generation in `reporter.py`
3. Add corresponding tests

## Deployment

### Browser Extension
1. Test thoroughly in developer mode
2. Create icons and screenshots
3. Submit to Chrome Web Store
4. Follow Chrome Web Store policies

### CLI Tool
1. Package for PyPI: `python setup.py sdist bdist_wheel`
2. Upload to PyPI: `twine upload dist/*`
3. Test installation: `pip install privacylens`

## Future Enhancements

### Planned Features
- 🔒 **Privacy Policy Analysis**: NLP analysis of privacy policies
- 🌍 **GDPR Compliance Check**: EU privacy regulation compliance
- 📱 **Mobile App**: React Native or Flutter app
- 🏢 **Enterprise Version**: Bulk analysis and reporting
- 🔄 **Continuous Monitoring**: Scheduled privacy audits
- 🤖 **Machine Learning**: AI-powered privacy risk detection

### Technical Improvements
- WebAssembly for faster analysis
- Real-time collaboration features
- Advanced reporting with charts
- Integration with security tools
- API for third-party integrations
