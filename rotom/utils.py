"""
Utility functions for ROTOM application
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os

def generate_event_poster(event):
    """
    Generate a highly attractive 1080x1920 poster for the event (Story format).
    """
    if not event.image:
        return None

    try:
        # Story dimensions (9:16 ratio)
        width, height = 1080, 1920
        # Create base image with ROTOM Green
        poster = Image.new('RGB', (width, height), color=(28, 101, 27))
        draw = ImageDraw.Draw(poster)

        # 1. Background Image (Full height with dark overlay)
        bg_img = Image.open(event.image)
        bg_img = ImageOps.exif_transpose(bg_img)
        bg_width, bg_height = bg_img.size
        scale = max(width / bg_width, height / bg_height)
        new_size = (int(bg_width * scale), int(bg_height * scale))
        bg_img = bg_img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Center crop
        left = (new_size[0] - width) / 2
        top = (new_size[1] - height) / 2
        bg_img = bg_img.crop((left, top, left + width, top + height))
        
        # Apply a subtle blur to the background for a modern look
        bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=2))
        poster.paste(bg_img, (0, 0))

        # 2. Modern Overlays
        # Bottom dark gradient for text readability
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Stronger gradient at the bottom
        for i in range(height // 2, height):
            alpha = int(220 * ((i - height // 2) / (height // 2)))
            overlay_draw.line([(0, i), (width, i)], fill=(0, 0, 0, alpha))
            
        # Subtle gradient at the top for the logo
        for i in range(300):
            alpha = int(150 * (1 - i / 300))
            overlay_draw.line([(0, i), (width, i)], fill=(0, 0, 0, alpha))
            
        poster.paste(overlay, (0, 0), overlay)

        # 3. Decorative Frame/Elements
        # Gold accent border
        border_margin = 40
        draw.rectangle([border_margin, border_margin, width - border_margin, height - border_margin], outline=(241, 201, 59), width=4)

        # 4. Typography Setup
        font_paths = [
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\segoeuib.ttf",
            "C:\\Windows\\Fonts\\georgiab.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        
        f_logo = f_title = f_badge = f_date = f_cta = None
        for path in font_paths:
            if os.path.exists(path):
                f_logo = ImageFont.truetype(path, 60)
                f_title = ImageFont.truetype(path, 110)
                f_badge = ImageFont.truetype(path, 32)
                f_date = ImageFont.truetype(path, 54)
                f_cta = ImageFont.truetype(path, 64)
                break
        
        if not f_logo:
            f_logo = f_title = f_badge = f_date = f_cta = ImageFont.load_default()

        # 5. Header: Logo & Branding
        draw.text((width // 2, 120), "ROTOM ETHIOPIA", fill=(241, 201, 59), font=f_logo, anchor="mt")
        draw.line([(width // 2 - 150, 190), (width // 2 + 150, 190)], fill=(241, 201, 59), width=3)

        # 6. Center: Event Title (Large and Bold)
        title_y = height // 2
        words = event.title.upper().split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            w = f_title.getlength(test_line) if hasattr(f_title, 'getlength') else draw.textbbox((0,0), test_line, font=f_title)[2]
            if w < (width - 200):
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        # Calculate total height of title to center it better
        line_height = 130
        title_total_height = len(lines) * line_height
        current_y = height - title_total_height - 600
        
        for line in lines:
            # Draw shadow
            draw.text((width // 2 + 4, current_y + 4), line, fill=(0, 0, 0, 180), font=f_title, anchor="mt")
            # Draw main text
            draw.text((width // 2, current_y), line, fill=(255, 255, 255), font=f_title, anchor="mt")
            current_y += line_height

        # 7. Badge: "UPCOMING EVENT" (Stylish Pill)
        badge_y = current_y - 20
        badge_w, badge_h = 400, 70
        badge_x = (width - badge_w) // 2
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=35, fill=(241, 201, 59))
        draw.text((width // 2, badge_y + 15), "UPCOMING EVENT", fill=(28, 101, 27), font=f_badge, anchor="mt")

        # 8. Date & Location Info
        info_y = badge_y + 150
        event_date_str = event.event_date.strftime("%A, %B %d, %Y").upper()
        # Draw date with icon placeholder
        draw.text((width // 2, info_y), f"📅 {event_date_str}", fill=(241, 201, 59), font=f_date, anchor="mt")
        draw.text((width // 2, info_y + 80), "📍 BISHOFTU, ETHIOPIA", fill=(255, 255, 255), font=f_date, anchor="mt")

        # 9. CTA Button: "JOIN THE MISSION" (Vibrant)
        cta_w, cta_h = 800, 140
        cta_x, cta_y = (width - cta_w) // 2, height - 300
        # Button Shadow
        draw.rounded_rectangle([cta_x + 5, cta_y + 5, cta_x + cta_w + 5, cta_y + cta_h + 5], radius=20, fill=(0, 0, 0, 100))
        # Button Main
        draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=20, fill=(241, 201, 59))
        draw.text((width // 2, cta_y + 35), "JOIN THE MISSION", fill=(28, 101, 27), font=f_cta, anchor="mt")

        # 10. Footer Website
        draw.text((width // 2, height - 100), "WWW.ROTOMETHIOPIA.ORG", fill=(255, 255, 255, 180), font=f_badge, anchor="mt")

        # 11. Save to BytesIO
        output = BytesIO()
        poster.save(output, format='JPEG', quality=95, optimize=True)
        output.seek(0)
        
        new_name = f"story_poster_{event.pk or 'new'}.jpg"
        return InMemoryUploadedFile(output, 'ImageField', new_name, 'image/jpeg', sys.getsizeof(output), None)

    except Exception as e:
        print(f"Poster generation failed: {e}")
        return None


def compress_image(image_field, max_width=1920, max_height=1080, quality=85):
    """
    Compress and resize uploaded images automatically.
    
    Args:
        image_field: Django ImageField
        max_width: Maximum width in pixels (default: 1920)
        max_height: Maximum height in pixels (default: 1080)
        quality: JPEG quality 1-100 (default: 85)
    
    Returns:
        Compressed image file
    """
    if not image_field:
        return image_field
    
    try:
        # Open the image
        img = Image.open(image_field)
        
        # Handle EXIF orientation (fixes rotated portrait images)
        img = ImageOps.exif_transpose(img)
        
        # Convert RGBA to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get original dimensions
        width, height = img.size
        
        # Calculate new dimensions while maintaining aspect ratio
        if width > max_width or height > max_height:
            # Calculate scaling factor
            width_ratio = max_width / width
            height_ratio = max_height / height
            ratio = min(width_ratio, height_ratio)
            
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # Resize image with high-quality resampling
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to BytesIO
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        # Get original filename and change extension to .jpg
        original_name = image_field.name
        name_without_ext = original_name.rsplit('.', 1)[0]
        new_name = f"{name_without_ext}.jpg"
        
        # Create new InMemoryUploadedFile
        compressed_image = InMemoryUploadedFile(
            output,
            'ImageField',
            new_name,
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
        
        return compressed_image
        
    except Exception as e:
        # If compression fails, return original image
        print(f"Image compression failed: {e}")
        return image_field


def compress_image_thumbnail(image_field, max_width=800, max_height=600, quality=80):
    """
    Create a smaller thumbnail version of the image.
    
    Args:
        image_field: Django ImageField
        max_width: Maximum width in pixels (default: 800)
        max_height: Maximum height in pixels (default: 600)
        quality: JPEG quality 1-100 (default: 80)
    
    Returns:
        Compressed thumbnail image file
    """
    return compress_image(image_field, max_width, max_height, quality)
