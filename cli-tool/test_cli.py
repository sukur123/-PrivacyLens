#!/usr/bin/env python3
"""
Test script for PrivacyLens CLI tool
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analyzer import PrivacyAnalyzer
from reporter import Reporter

def test_basic_functionality():
    """Test basic analyzer functionality"""
    print("🧪 Testing PrivacyLens CLI components...")
    
    # Test analyzer initialization
    try:
        analyzer = PrivacyAnalyzer(timeout=5, verbose=True)
        print("✅ Analyzer initialized successfully")
    except Exception as e:
        print(f"❌ Analyzer initialization failed: {e}")
        return False
    
    # Test reporter initialization
    try:
        reporter = Reporter(output_format='text')
        print("✅ Reporter initialized successfully")
    except Exception as e:
        print(f"❌ Reporter initialization failed: {e}")
        return False
    
    # Test with a simple URL (example.com)
    test_url = "https://example.com"
    print(f"\n🔍 Testing analysis with {test_url}")
    
    try:
        # Perform analysis
        result = analyzer.analyze(test_url)
        print("✅ Analysis completed successfully")
        
        # Generate report
        report = reporter.generate_report(result)
        print("✅ Report generated successfully")
        
        # Show basic results
        score = result.get('privacy_score', 0)
        print(f"\n📊 Test Results:")
        print(f"   Privacy Score: {score}/100")
        print(f"   Domain: {result.get('domain', 'N/A')}")
        
        if score >= 70:
            print("✅ Test completed successfully!")
            return True
        else:
            print("⚠️  Test completed with warnings (low score expected for example.com)")
            return True
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
