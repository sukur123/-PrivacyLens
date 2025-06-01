# 🎨 Icon Suggestions for PrivacyLens

## Main Logo/Icons
For creating the browser extension icons and general branding, here are some visual concepts:

### Primary Icon Design
- **Base**: Shield shape (🛡️) with a magnifying glass (🔍)
- **Colors**: 
  - Primary: Deep blue (#2c3e50) or purple (#667eea)
  - Accent: Green (#27ae60) for good privacy, Red (#e74c3c) for poor privacy
  - Background: White or transparent

### Icon Variations by Privacy Score
- **High Privacy (80-100)**: Green shield with checkmark ✅
- **Medium Privacy (50-79)**: Yellow/orange shield with warning ⚠️
- **Low Privacy (0-49)**: Red shield with X mark ❌

### Recommended Icon Resources
1. **Heroicons** (https://heroicons.com/):
   - shield-check, shield-exclamation, eye, lock-closed
2. **Feather Icons** (https://feathericons.com/):
   - shield, eye, lock, alert-triangle
3. **Material Design Icons**:
   - security, visibility, lock, warning

### Size Requirements
- 16x16: Favicon and browser tab
- 32x32: Extension popup
- 48x48: Extension management page
- 128x128: Chrome Web Store

### Creation Tools
- **Figma** (free): Professional icon design
- **Canva**: Quick icon creation with templates
- **GIMP**: Free alternative to Photoshop
- **Inkscape**: Free vector graphics editor

### Color Palette
```css
/* Primary Colors */
--primary-blue: #2c3e50;
--secondary-purple: #667eea;
--accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Status Colors */
--success-green: #27ae60;
--warning-orange: #f39c12;
--danger-red: #e74c3c;
--info-blue: #3498db;

/* Neutral Colors */
--text-dark: #2c3e50;
--text-light: #7f8c8d;
--background-light: #ecf0f1;
--white: #ffffff;
```

## Implementation Notes
- Use SVG format for scalability
- Ensure icons work on both light and dark backgrounds
- Test visibility at small sizes (16x16)
- Follow platform-specific design guidelines (Material Design for Chrome)
