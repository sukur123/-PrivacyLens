// Background service worker for PrivacyLens
console.log('PrivacyLens background service worker loaded');

// Storage for analysis data
let analysisCache = new Map();

// Initialize extension
chrome.runtime.onInstalled.addListener((details) => {
    console.log('PrivacyLens installed:', details);
    
    // Set default settings
    chrome.storage.local.set({
        settings: {
            enableRealTimeAnalysis: true,
            showNotifications: true,
            autoBlock: false
        }
    });
});

// Tab update listener for real-time analysis
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {
        // Trigger analysis after page load
        setTimeout(() => {
            performBackgroundAnalysis(tabId, tab.url);
        }, 2000);
    }
});

// Message listener for popup communication
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getAnalysisData') {
        const data = analysisCache.get(sender.tab?.id);
        sendResponse(data || null);
    } else if (request.action === 'updateAnalysisData') {
        analysisCache.set(sender.tab?.id, request.data);
        
        // Update badge with privacy score
        updateBadge(sender.tab?.id, request.data.score);
        
        sendResponse({ success: true });
    }
    return true;
});

// Perform background analysis
async function performBackgroundAnalysis(tabId, url) {
    try {
        // Inject content script if not already present
        await chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ['background/content.js']
        });
        
        console.log('Background analysis triggered for:', url);
    } catch (error) {
        console.error('Failed to inject content script:', error);
    }
}

// Update extension badge
function updateBadge(tabId, score) {
    if (!tabId || score === undefined) return;
    
    let badgeColor = '#4CAF50'; // Green
    let badgeText = String(score);
    
    if (score < 70) {
        badgeColor = '#FF9800'; // Orange
    }
    if (score < 50) {
        badgeColor = '#F44336'; // Red
    }
    
    chrome.action.setBadgeBackgroundColor({ color: badgeColor, tabId });
    chrome.action.setBadgeText({ text: badgeText, tabId });
}

// Cookie analysis helper
async function analyzeCookies(tabId, url) {
    try {
        const cookies = await chrome.cookies.getAll({ url });
        
        const analysis = {
            total: cookies.length,
            tracking: 0,
            functional: 0,
            session: 0,
            persistent: 0,
            items: []
        };
        
        cookies.forEach(cookie => {
            // Classify cookies based on name and domain
            const isTracking = isTrackingCookie(cookie);
            if (isTracking) {
                analysis.tracking++;
            } else {
                analysis.functional++;
            }
            
            if (cookie.session) {
                analysis.session++;
            } else {
                analysis.persistent++;
            }
            
            analysis.items.push({
                name: cookie.name,
                domain: cookie.domain,
                isTracking,
                isSession: cookie.session,
                secure: cookie.secure,
                httpOnly: cookie.httpOnly
            });
        });
        
        return analysis;
    } catch (error) {
        console.error('Cookie analysis failed:', error);
        return { total: 0, tracking: 0, functional: 0, session: 0, persistent: 0, items: [] };
    }
}

// Check if cookie is tracking-related
function isTrackingCookie(cookie) {
    const trackingPatterns = [
        '_ga', '_gid', '_gtm', 'fbp', 'fbq', '_fbp',
        'NID', 'IDE', '__utma', '__utmb', '__utmc', '__utmz',
        'fr', 'tr', 'personalization_id', 'guest_id'
    ];
    
    const trackingDomains = [
        'google-analytics.com', 'googletagmanager.com', 
        'facebook.com', 'doubleclick.net', 'googlesyndication.com',
        'twitter.com', 'linkedin.com', 'amazon-adsystem.com'
    ];
    
    return trackingPatterns.some(pattern => cookie.name.includes(pattern)) ||
           trackingDomains.some(domain => cookie.domain.includes(domain));
}

// Clear cache when tab is closed
chrome.tabs.onRemoved.addListener((tabId) => {
    analysisCache.delete(tabId);
});

// Privacy score calculator (server-side)
function calculatePrivacyScore(analysisData) {
    let score = 100;
    
    // Deduct points based on privacy risks
    if (analysisData.cookies) {
        score -= analysisData.cookies.tracking * 1;
        score -= analysisData.cookies.functional * 0.5;
    }
    
    if (analysisData.scripts) {
        score -= analysisData.scripts.tracking * 2;
        score -= analysisData.scripts.analytics * 1.5;
    }
    
    if (analysisData.storage) {
        score -= analysisData.storage.localStorage * 1;
        score -= analysisData.storage.sessionStorage * 0.5;
    }
    
    if (analysisData.iframes) {
        score -= analysisData.iframes.thirdParty * 3;
    }
    
    return Math.max(0, Math.min(100, Math.round(score)));
}
