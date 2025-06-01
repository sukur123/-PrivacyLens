"""
Utility functions for PrivacyLens CLI
"""

import re
from urllib.parse import urlparse


def validate_url(url):
    """Validate URL format"""
    if not url:
        return False
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def normalize_url(url):
    """Normalize URL by adding scheme if missing"""
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url


def extract_domain(url):
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return None


def is_valid_domain(domain):
    """Check if domain name is valid"""
    if not domain:
        return False
    
    # Basic domain validation
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )
    
    return bool(pattern.match(domain))


def format_bytes(bytes_count):
    """Format bytes into human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"


def truncate_string(text, max_length=50):
    """Truncate string with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def get_score_color_code(score):
    """Get ANSI color code for score"""
    if score >= 80:
        return '\033[92m'  # Green
    elif score >= 60:
        return '\033[93m'  # Yellow
    elif score >= 40:
        return '\033[95m'  # Magenta
    else:
        return '\033[91m'  # Red


def reset_color():
    """Get ANSI reset color code"""
    return '\033[0m'
