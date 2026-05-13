"""
Utility functions for ROTOM application
"""
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


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
