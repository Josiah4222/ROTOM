"""
Utility functions for ROTOM application
"""
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(image_field, max_width=1920, max_height=1080, quality=80):
    """
    Compress and resize uploaded images automatically, converting to WebP for best performance.
    """
    if not image_field:
        return image_field
    
    try:
        # Open the image
        img = Image.open(image_field)
        
        # Handle transparency for WebP
        if img.mode in ('RGBA', 'LA', 'P'):
            if img.mode == 'P':
                img = img.convert('RGBA')
            # Keep RGBA for WebP to preserve transparency
        else:
            img = img.convert('RGB')
        
        # Get original dimensions
        width, height = img.size
        
        # Calculate new dimensions while maintaining aspect ratio
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to BytesIO as WebP
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality, method=6)
        output.seek(0)
        
        # Get original filename and change extension to .webp
        original_name = image_field.name
        name_without_ext = original_name.rsplit('.', 1)[0]
        new_name = f"{name_without_ext}.webp"
        
        # Create new InMemoryUploadedFile
        compressed_image = InMemoryUploadedFile(
            output,
            'ImageField',
            new_name,
            'image/webp',
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
