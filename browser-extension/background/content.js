// Content script for privacy analysis
console.log('PrivacyLens content script loaded');

// Privacy analyzer class
class ContentPrivacyAnalyzer {
    constructor() {
        this.analysisData = {
            cookies: { count: 0, tracking: 0, functional: 0, items: [] },
            scripts: { count: 0, tracking: 0, analytics: 0, items: [] },
            storage: { localStorage: 0, sessionStorage: 0, items: [] },
            iframes: { count: 0, thirdParty: 0, items: [] },
            fingerprinting: { canvas: false, webgl: false, fonts: false },
            url: window.location.href,
            domain: window.location.hostname,
            timestamp: Date.now()
        };
    }

    async analyze() {
        console.log('Starting privacy analysis...');
        
        try {
            await this.analyzeCookies();
            this.analyzeScripts();
            this.analyzeStorage();
            this.analyzeIframes();
            this.analyzeFingerprinting();
            
            // Send data to background script
            chrome.runtime.sendMessage({
                action: 'updateAnalysisData',
                data: this.analysisData
            });
            
            console.log('Privacy analysis completed:', this.analysisData);
            return this.analysisData;
        } catch (error) {
            console.error('Privacy analysis failed:', error);
            return this.analysisData;
        }
    }

    async analyzeCookies() {
        // Get all cookies for current domain
        const cookies = document.cookie.split(';').filter(c => c.trim());
        
        this.analysisData.cookies.count = cookies.length;
        
        cookies.forEach(cookie => {
            const [name] = cookie.trim().split('=');
            const isTracking = this.isTrackingCookie(name);
            
            if (isTracking) {
                this.analysisData.cookies.tracking++;
            } else {
                this.analysisData.cookies.functional++;
            }
            
            this.analysisData.cookies.items.push({
                name: name,
                isTracking: isTracking
            });
        });
    }

    analyzeScripts() {
        const scripts = document.querySelectorAll('script[src]');
        this.analysisData.scripts.count = scripts.length;
        
        scripts.forEach(script => {
            const src = script.src;
            const scriptInfo = this.classifyScript(src);
            
            if (scriptInfo.isTracking) {
                this.analysisData.scripts.tracking++;
            }
            if (scriptInfo.isAnalytics) {
                this.analysisData.scripts.analytics++;
            }
            
            this.analysisData.scripts.items.push({
                src: src,
                domain: this.extractDomain(src),
                type: scriptInfo.type,
                isThirdParty: !src.includes(window.location.hostname)
            });
        });
    }

    analyzeStorage() {
        // Analyze localStorage
        try {
            this.analysisData.storage.localStorage = localStorage.length;
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                this.analysisData.storage.items.push({
                    key: key,
                    type: 'localStorage',
                    size: localStorage.getItem(key)?.length || 0
                });
            }
        } catch (error) {
            console.warn('localStorage access denied:', error);
        }

        // Analyze sessionStorage
        try {
            this.analysisData.storage.sessionStorage = sessionStorage.length;
            for (let i = 0; i < sessionStorage.length; i++) {
                const key = sessionStorage.key(i);
                this.analysisData.storage.items.push({
                    key: key,
                    type: 'sessionStorage',
                    size: sessionStorage.getItem(key)?.length || 0
                });
            }
        } catch (error) {
            console.warn('sessionStorage access denied:', error);
        }
    }

    analyzeIframes() {
        const iframes = document.querySelectorAll('iframe');
        this.analysisData.iframes.count = iframes.length;
        
        iframes.forEach(iframe => {
            const src = iframe.src;
            const isThirdParty = src && !src.includes(window.location.hostname);
            
            if (isThirdParty) {
                this.analysisData.iframes.thirdParty++;
            }
            
            this.analysisData.iframes.items.push({
                src: src,
                domain: this.extractDomain(src),
                isThirdParty: isThirdParty,
                sandbox: iframe.hasAttribute('sandbox')
            });
        });
    }

    analyzeFingerprinting() {
        // Check for canvas fingerprinting
        const canvasElements = document.querySelectorAll('canvas');
        if (canvasElements.length > 0) {
            this.analysisData.fingerprinting.canvas = true;
        }
        
        // Check for WebGL fingerprinting
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (gl) {
                this.analysisData.fingerprinting.webgl = true;
            }
        } catch (error) {
            // WebGL not available
        }
        
        // Check for font detection
        const fontsToCheck = ['Arial', 'Times New Roman', 'Courier New', 'Georgia', 'Verdana'];
        let detectedFonts = 0;
        
        fontsToCheck.forEach(font => {
            const element = document.createElement('span');
            element.style.font = `12px ${font}`;
            element.textContent = 'test';
            document.body.appendChild(element);
            
            if (element.offsetWidth > 0) {
                detectedFonts++;
            }
            
            document.body.removeChild(element);
        });
        
        this.analysisData.fingerprinting.fonts = detectedFonts > 3;
    }

    isTrackingCookie(name) {
        const trackingPatterns = [
            '_ga', '_gid', '_gtm', 'fbp', 'fbq', '_fbp',
            'NID', 'IDE', '__utma', '__utmb', '__utmc', '__utmz',
            'fr', 'tr', 'personalization_id', 'guest_id'
        ];
        
        return trackingPatterns.some(pattern => name.includes(pattern));
    }

    classifyScript(src) {
        const trackingServices = {
            'google-analytics.com': { type: 'analytics', isTracking: true, isAnalytics: true },
            'googletagmanager.com': { type: 'analytics', isTracking: true, isAnalytics: true },
            'facebook.com': { type: 'social', isTracking: true, isAnalytics: false },
            'facebook.net': { type: 'social', isTracking: true, isAnalytics: false },
            'doubleclick.net': { type: 'advertising', isTracking: true, isAnalytics: false },
            'googlesyndication.com': { type: 'advertising', isTracking: true, isAnalytics: false },
            'twitter.com': { type: 'social', isTracking: true, isAnalytics: false },
            'linkedin.com': { type: 'social', isTracking: true, isAnalytics: false },
            'amazon-adsystem.com': { type: 'advertising', isTracking: true, isAnalytics: false },
            'hotjar.com': { type: 'analytics', isTracking: true, isAnalytics: true },
            'mixpanel.com': { type: 'analytics', isTracking: true, isAnalytics: true }
        };
        
        for (const [domain, info] of Object.entries(trackingServices)) {
            if (src.includes(domain)) {
                return info;
            }
        }
        
        return { type: 'unknown', isTracking: false, isAnalytics: false };
    }

    extractDomain(url) {
        try {
            return new URL(url).hostname;
        } catch {
            return 'unknown';
        }
    }
}

// Message listener
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyzePrivacy') {
        const analyzer = new ContentPrivacyAnalyzer();
        analyzer.analyze().then(result => {
            sendResponse(result);
        });
        return true; // Keep message port open for async response
    }
});

// Auto-analyze when page loads
window.addEventListener('load', () => {
    setTimeout(() => {
        const analyzer = new ContentPrivacyAnalyzer();
        analyzer.analyze();
    }, 1000);
});

// Monitor dynamic changes
const observer = new MutationObserver((mutations) => {
    let shouldReanalyze = false;
    
    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE) {
                if (node.tagName === 'SCRIPT' || node.tagName === 'IFRAME') {
                    shouldReanalyze = true;
                }
            }
        });
    });
    
    if (shouldReanalyze) {
        setTimeout(() => {
            const analyzer = new ContentPrivacyAnalyzer();
            analyzer.analyze();
        }, 500);
    }
});

// Start observing
observer.observe(document.body, {
    childList: true,
    subtree: true
});
