# Partner Management Guide

## Overview
You can now manage the "Our Partners" section on your homepage directly from the admin dashboard. Add, edit, delete, and reorder partner logos without touching any code!

## Accessing Partner Management

1. Log in to your admin dashboard at: `/admin/`
2. Look for **"Partners"** in the ROTOM section
3. Click to view all partners

## Adding a New Partner

1. Click **"Add Partner"** button
2. Fill in the form:
   - **Name**: Partner organization name (e.g., "UNICEF Ethiopia")
   - **Logo**: Upload partner logo image
     - Recommended: Transparent PNG
     - Recommended size: Square (200x200px) or landscape (300x150px)
     - Keep under 500KB for best performance
   - **Website**: Partner website URL (optional)
     - If provided, logo will be clickable
     - Opens in new tab
   - **Description**: Brief description of partnership (optional)
     - For internal reference
     - Not displayed on website
   - **Order**: Display order number
     - Lower numbers appear first
     - Use increments of 10 (10, 20, 30) for easy reordering
   - **Is Active**: Check to display on website
     - Uncheck to hide without deleting

3. Click **"Save"**

## Editing a Partner

1. Click on the partner name in the list
2. Modify any fields:
   - Change logo
   - Update name
   - Add/edit website
   - Change order
   - Activate/deactivate
3. Click "Save"
4. Refresh your website to see changes

## Deleting a Partner

### Soft Delete (Recommended)
1. Click on the partner name
2. Uncheck "Is Active"
3. Click "Save"
- Partner is hidden but data is preserved
- Can be reactivated later

### Permanent Delete
1. Click on the partner name
2. Click "Delete" button at bottom
3. Confirm deletion
- Partner and logo are permanently removed
- Cannot be undone

## Reordering Partners

### Method 1: Edit Order Numbers
1. Click on each partner
2. Change the "Order" field
3. Save
- Lower numbers appear first
- Use increments of 10 for flexibility

### Method 2: Bulk Edit (Quick)
1. Go to Partners list
2. Click the "Order" column header to sort
3. Edit order numbers directly in the list
4. Changes save automatically

## Managing Partner Display

### Show/Hide Partners
- Check/uncheck "Is Active" in the list view
- Changes save automatically
- Hidden partners remain in database

### Partner Slider
- Partners automatically scroll in a slider
- Slider duplicates logos for continuous effect
- Works on all screen sizes

## Logo Guidelines

### Image Format
- **Best**: PNG with transparent background
- **Good**: JPG or WEBP
- **Avoid**: GIF or BMP

### Image Size
- **Square logos**: 200x200px to 400x400px
- **Landscape logos**: 300x150px to 600x300px
- **File size**: Under 500KB (compress if needed)

### Image Quality
- High resolution for retina displays
- Clean, professional appearance
- Good contrast with white background

## Current Partners

Your existing 13 partners have been migrated:
1. HFT Foundation
2. Holland Foundation
3. ROTOM USA
4. Canada Partnership
5. GK Organization
6. AHSAM
7. Andu Foundation
8. Alfa Organization
9. Beautiful World
10. EDF
11. Global Care
12. Maranatha
13. Pyramid Foundation

## Features

✅ **Add/Edit/Delete** - Full CRUD operations
✅ **Reorder** - Control display order
✅ **Show/Hide** - Activate/deactivate without deleting
✅ **Clickable Logos** - Optional website links
✅ **Auto Slider** - Automatic scrolling animation
✅ **Responsive** - Works on all devices
✅ **Fast Loading** - Optimized for performance

## Tips for Best Results

### Organization
- Use order numbers in increments of 10 (10, 20, 30...)
- This allows easy insertion between partners
- Example: To add between 20 and 30, use 25

### Naming
- Use full organization names
- Be consistent with capitalization
- Include country if needed (e.g., "UNICEF Ethiopia")

### Logos
- Ensure logos are clear and readable
- Test on both light and dark backgrounds
- Compress images before uploading

### Website Links
- Always use full URLs (https://example.com)
- Test links after adding
- Use official partner websites only

## Troubleshooting

### Partner not showing on website
1. Check "Is Active" is checked
2. Verify logo uploaded successfully
3. Hard refresh browser: `Ctrl + Shift + F5`
4. Clear browser cache

### Logo looks distorted
- Check original image dimensions
- Use square or landscape format
- Avoid portrait orientation

### Slider not working
- Ensure at least 3 partners are active
- Check browser console for errors
- Clear cache and refresh

### Logo not clickable
- Verify website URL is entered
- Check URL format (must include https://)
- Test link in new tab

## Admin Interface Features

### List View
- **Name**: Partner organization name
- **Order**: Display order number (editable)
- **Is Active**: Show/hide toggle (editable)
- **Website**: Checkmark if URL provided
- **Created At**: When partner was added

### Filters
- Filter by active/inactive status
- Filter by creation date
- Search by name or description

### Bulk Actions
- Delete multiple partners at once
- Use checkboxes to select
- Choose action from dropdown

## Technical Details

### Database Model
- **Model**: `Partner`
- **Location**: `rotom/models.py`
- **Upload Directory**: `media/partners/`

### Template Integration
- **Template**: `rotom/templates/rotom/index.html`
- **Section**: `#partners`
- **View**: `home()` in `rotom/views.py`

### How It Works
1. Partners are stored in database with logos
2. Active partners are loaded in home view
3. Template displays partners in slider
4. Slider auto-scrolls with CSS animation
5. Logos link to websites if provided

## Best Practices

### Before Adding
1. Get permission to use partner logo
2. Obtain high-quality logo file
3. Verify website URL is correct
4. Compress image if over 500KB

### Regular Maintenance
1. Review partners quarterly
2. Update logos if partners rebrand
3. Remove inactive partnerships
4. Keep order logical (by importance or alphabetical)

### Performance
1. Keep total partners under 30
2. Compress all logo images
3. Use PNG for transparency
4. Optimize file sizes

## Need Help?

If you encounter any issues:
1. Check this guide for solutions
2. Review admin dashboard for error messages
3. Test on different browsers
4. Contact your developer for technical support

---

**Last Updated**: May 5, 2026
