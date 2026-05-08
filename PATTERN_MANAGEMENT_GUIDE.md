# Navbar Pattern Management Guide

## Overview
You can now manage the Ethiopian pattern bar below your navbar directly from the admin dashboard. Upload new patterns, adjust their height and opacity, and switch between them without touching any code!

## Accessing Pattern Management

1. Log in to your admin dashboard at: `/admin/`
2. Look for **"Navbar Patterns"** in the ROTOM section
3. Click to view all patterns

## Adding a New Pattern

1. Click **"Add Navbar Pattern"** button
2. Fill in the form:
   - **Name**: Give your pattern a descriptive name (e.g., "Blue Ethiopian Pattern")
   - **Image**: Upload your pattern image file
     - Recommended: Horizontal repeating pattern
     - Formats: PNG, JPG, or WEBP
     - Size: Keep under 500KB for best performance
   - **Height**: Pattern bar height in pixels (default: 60)
     - Typical range: 40-80 pixels
   - **Opacity**: Pattern transparency (0.00 to 1.00)
     - 0.00 = completely transparent
     - 1.00 = completely opaque
     - Default: 0.80 (80% visible)
   - **Is Active**: Check this box to use this pattern on the navbar
     - ⚠️ Only ONE pattern can be active at a time
     - Checking this will automatically deactivate other patterns

3. Click **"Save"**

## Switching Between Patterns

### Method 1: From the List View
1. Go to the Navbar Patterns list
2. Check the "Is Active" checkbox for the pattern you want to use
3. The page will save automatically
4. Refresh your website to see the new pattern

### Method 2: From the Edit View
1. Click on the pattern you want to activate
2. Check the "Is Active" checkbox
3. Click "Save"
4. Refresh your website to see the new pattern

## Editing an Existing Pattern

1. Click on the pattern name in the list
2. Modify any fields:
   - Change the image
   - Adjust height
   - Adjust opacity
   - Activate/deactivate
3. Click "Save"
4. Refresh your website to see changes

## Tips for Best Results

### Pattern Image Guidelines
- **Horizontal repeating patterns work best** - the image will repeat horizontally across the screen
- **Seamless patterns** - make sure the left and right edges match for smooth repetition
- **Appropriate height** - if your pattern is 100px tall, set the height to 100px
- **Optimize file size** - compress images before uploading

### Height Recommendations
- **Small/Subtle**: 30-40px
- **Medium/Standard**: 50-70px (recommended)
- **Large/Bold**: 80-100px

### Opacity Recommendations
- **Very Subtle**: 0.30-0.50
- **Balanced**: 0.60-0.80 (recommended)
- **Bold**: 0.85-1.00

## Current Pattern

Your current pattern has been migrated to the database:
- **Name**: Green Ethiopian Pattern
- **Height**: 60px
- **Opacity**: 0.80
- **Status**: Active

## Troubleshooting

### Pattern not showing on website
1. Make sure the pattern is marked as "Active"
2. Hard refresh your browser: `Ctrl + Shift + F5` (Windows) or `Cmd + Shift + R` (Mac)
3. Clear your browser cache
4. Check that the image file uploaded successfully

### Pattern looks stretched or distorted
- Adjust the height to match your image's natural height
- Use a different image with better dimensions

### Pattern is too visible/not visible enough
- Adjust the opacity value
- 0.50 = 50% transparent
- 0.80 = 20% transparent (80% visible)
- 1.00 = fully visible

### Multiple patterns showing
- This shouldn't happen, but if it does:
  1. Go to Navbar Patterns list
  2. Uncheck "Is Active" for all patterns except the one you want
  3. Save changes

## Technical Details

### Database Model
- **Model**: `NavbarPattern`
- **Location**: `rotom/models.py`
- **Upload Directory**: `media/patterns/`

### How It Works
1. Patterns are stored in the database with their settings
2. The active pattern is loaded via a context processor
3. The navbar template dynamically applies the pattern's image, height, and opacity
4. Only one pattern can be active at a time (enforced by the model)

### Files Modified
- `rotom/models.py` - Added NavbarPattern model
- `rotom/admin.py` - Added admin interface
- `rotom/context_processors.py` - Added pattern context processor
- `rotom/templates/rotom/navbar.html` - Made pattern dynamic
- `static/css/navbar.css` - Removed hardcoded values
- `REACHONEETH/settings.py` - Registered context processor

## Need Help?

If you encounter any issues or need assistance:
1. Check the admin dashboard for error messages
2. Review this guide for common solutions
3. Contact your developer for technical support

---

**Last Updated**: May 5, 2026
