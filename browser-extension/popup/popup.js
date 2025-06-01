// Privacy analysis data
let currentAnalysis = {
    score: 0,
    cookies: { count: 0, tracking: 0, functional: 0, items: [] },
    scripts: { count: 0, tracking: 0, analytics: 0, items: [] },
    storage: { localStorage: 0, sessionStorage: 0, items: [] },
    iframes: { count: 0, thirdParty: 0, items: [] },
    recommendations: []
};

// Privacy score calculator
class PrivacyScoreCalculator {
    static calculate(analysis) {
        let score = 100;
        
        // Cookies deduction
        score -= analysis.cookies.tracking * 1;
        score -= analysis.cookies.functional * 0.5;
        
        // Third-party scripts deduction
        score -= analysis.scripts.tracking * 2;
        score -= analysis.scripts.analytics * 1.5;
        
        // Storage deduction
        score -= analysis.storage.localStorage * 1;
        score -= analysis.storage.sessionStorage * 0.5;
        
        // Iframes deduction
        score -= analysis.iframes.thirdParty * 3;
        
        return Math.max(0, Math.min(100, Math.round(score)));
    }
    
    static getScoreStatus(score) {
        if (score >= 90) return { class: 'score-excellent', text: 'Excellent Privacy' };
        if (score >= 70) return { class: 'score-good', text: 'Good Privacy' };
        if (score >= 50) return { class: 'score-moderate', text: 'Moderate Privacy' };
        return { class: 'score-poor', text: 'Poor Privacy' };
    }
}

// Privacy analyzer
class PrivacyAnalyzer {
    static async analyzeCurrentTab() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            if (!tab) return;

            // Get analysis data from content script
            const result = await chrome.tabs.sendMessage(tab.id, { action: 'analyzePrivacy' });
            
            if (result) {
                currentAnalysis = result;
                currentAnalysis.score = PrivacyScoreCalculator.calculate(result);
                this.generateRecommendations();
                this.updateUI();
            }
        } catch (error) {
            console.error('Analysis failed:', error);
            this.showError('Failed to analyze page');
        }
    }

    static generateRecommendations() {
        const recommendations = [];
        
        if (currentAnalysis.cookies.tracking > 5) {
            recommendations.push({
                text: 'Consider using privacy-focused browser settings to block tracking cookies',
                priority: 'high'
            });
        }
        
        if (currentAnalysis.scripts.tracking > 3) {
            recommendations.push({
                text: 'Multiple tracking scripts detected. Use an ad blocker for better privacy',
                priority: 'high'
            });
        }
        
        if (currentAnalysis.storage.localStorage > 10) {
            recommendations.push({
                text: 'High amount of local storage usage. Clear browser data regularly',
                priority: 'medium'
            });
        }
        
        if (currentAnalysis.iframes.thirdParty > 0) {
            recommendations.push({
                text: 'Third-party iframes present. Be cautious of embedded content',
                priority: 'medium'
            });
        }
        
        if (recommendations.length === 0) {
            recommendations.push({
                text: 'Good privacy practices detected on this website',
                priority: 'low'
            });
        }
        
        currentAnalysis.recommendations = recommendations;
    }

    static updateUI() {
        // Update score
        const scoreValue = document.getElementById('scoreValue');
        const scoreStatus = document.getElementById('scoreStatus');
        const scoreCircle = document.getElementById('scoreCircle');
        
        scoreValue.textContent = currentAnalysis.score;
        
        const status = PrivacyScoreCalculator.getScoreStatus(currentAnalysis.score);
        scoreStatus.textContent = status.text;
        scoreStatus.className = `score-status ${status.class}`;
        
        // Update score circle color
        const percentage = currentAnalysis.score;
        let color = '#4caf50'; // Green
        if (percentage < 70) color = '#ff9800'; // Orange
        if (percentage < 50) color = '#f44336'; // Red
        
        scoreCircle.style.setProperty('--score-percent', `${percentage}%`);
        scoreCircle.style.background = `conic-gradient(from 0deg, ${color} 0%, ${color} ${percentage}%, #e0e0e0 ${percentage}%, #e0e0e0 100%)`;
        
        // Update risk items
        this.updateRiskItem('cookies', currentAnalysis.cookies);
        this.updateRiskItem('scripts', currentAnalysis.scripts);
        this.updateRiskItem('storage', currentAnalysis.storage);
        this.updateRiskItem('iframes', currentAnalysis.iframes);
        
        // Update recommendations
        this.updateRecommendations();
        
        // Update timestamp
        document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();
    }

    static updateRiskItem(type, data) {
        const item = document.getElementById(`${type}Risk`);
        const badge = document.getElementById(`${type}Badge`);
        const details = document.getElementById(`${type}Details`);
        
        let count = 0;
        let riskLevel = 'low-risk';
        let detailsHtml = '';
        
        switch (type) {
            case 'cookies':
                count = data.count;
                if (data.tracking > 5) riskLevel = 'high-risk';
                else if (data.tracking > 2) riskLevel = 'medium-risk';
                
                detailsHtml = `
                    <div>Tracking: ${data.tracking}, Functional: ${data.functional}</div>
                    ${data.items.length > 0 ? `<ul>${data.items.slice(0, 3).map(item => `<li>${item}</li>`).join('')}</ul>` : ''}
                `;
                break;
                
            case 'scripts':
                count = data.count;
                if (data.tracking > 3) riskLevel = 'high-risk';
                else if (data.tracking > 1) riskLevel = 'medium-risk';
                
                detailsHtml = `
                    <div>Tracking: ${data.tracking}, Analytics: ${data.analytics}</div>
                    ${data.items.length > 0 ? `<ul>${data.items.slice(0, 3).map(item => `<li>${item}</li>`).join('')}</ul>` : ''}
                `;
                break;
                
            case 'storage':
                count = data.localStorage + data.sessionStorage;
                if (count > 15) riskLevel = 'high-risk';
                else if (count > 5) riskLevel = 'medium-risk';
                
                detailsHtml = `
                    <div>localStorage: ${data.localStorage}, sessionStorage: ${data.sessionStorage}</div>
                `;
                break;
                
            case 'iframes':
                count = data.count;
                if (data.thirdParty > 2) riskLevel = 'high-risk';
                else if (data.thirdParty > 0) riskLevel = 'medium-risk';
                
                detailsHtml = `
                    <div>Third-party: ${data.thirdParty}, Total: ${data.count}</div>
                    ${data.items.length > 0 ? `<ul>${data.items.slice(0, 3).map(item => `<li>${item}</li>`).join('')}</ul>` : ''}
                `;
                break;
        }
        
        // Update badge
        badge.textContent = count;
        badge.className = `risk-badge ${riskLevel === 'high-risk' ? 'danger' : riskLevel === 'medium-risk' ? 'warning' : 'safe'}`;
        
        // Update item class
        item.className = `risk-item ${riskLevel}`;
        
        // Update details
        details.innerHTML = detailsHtml;
        
        // Add click handler to toggle details
        const header = item.querySelector('.risk-header');
        header.style.cursor = 'pointer';
        header.onclick = () => {
            details.classList.toggle('show');
        };
    }

    static updateRecommendations() {
        const list = document.getElementById('recommendationsList');
        
        if (currentAnalysis.recommendations.length === 0) {
            list.innerHTML = '<div class="recommendation-item">No specific recommendations at this time.</div>';
            return;
        }
        
        list.innerHTML = currentAnalysis.recommendations
            .map(rec => `
                <div class="recommendation-item priority-${rec.priority}">
                    ${rec.text}
                </div>
            `).join('');
    }

    static showError(message) {
        document.getElementById('scoreValue').textContent = '!';
        document.getElementById('scoreStatus').textContent = message;
        document.getElementById('scoreStatus').className = 'score-status score-poor';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initial analysis
    PrivacyAnalyzer.analyzeCurrentTab();
    
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', () => {
        document.getElementById('refreshBtn').style.animation = 'spin 1s linear';
        setTimeout(() => {
            document.getElementById('refreshBtn').style.animation = '';
        }, 1000);
        
        PrivacyAnalyzer.analyzeCurrentTab();
    });
});

// Add spin animation for refresh button
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
