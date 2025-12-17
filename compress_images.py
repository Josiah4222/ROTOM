"""
Script to compress large images in the static folder
Run: python compress_images.py
"""
from PIL import Image
import os

# Folders to scan for images
IMAGE_FOLDERS = [
    'static/images',
    'rotom/static/images',
    'media/event_images',
]

# Max dimension (width or height)
MAX_SIZE = 1200
# JPEG quality (1-100, lower = smaller file)
QUALITY = 75
# Minimum file size to compress (in bytes) - 500KB
MIN_SIZE_TO_COMPRESS = 500 * 1024

def compress_image(filepath):
    try:
        original_size = os.path.getsize(filepath)
        
        # Skip small files
        if original_size < MIN_SIZE_TO_COMPRESS:
            return False
        
        with Image.open(filepath) as img:
            # Convert to RGB if necessary (for JPEG)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if larger than MAX_SIZE
            width, height = img.size
            resized = False
            if width > MAX_SIZE or height > MAX_SIZE:
                if width > height:
                    new_width = MAX_SIZE
                    new_height = int(height * (MAX_SIZE / width))
                else:
                    new_height = MAX_SIZE
                    new_width = int(width * (MAX_SIZE / height))
                img = img.resize((new_width, new_height), Image.LANCZOS)
                resized = True
                print(f"  Resized: {width}x{height} -> {new_width}x{new_height}")
            
            # Save with compression
            output_path = filepath
            if filepath.lower().endswith('.png'):
                # Convert PNG to JPG for better compression
                output_path = filepath.rsplit('.', 1)[0] + '.jpg'
            
            img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
        
        new_size = os.path.getsize(output_path)
        reduction = ((original_size - new_size) / original_size) * 100
        
        print(f"  {original_size/1024/1024:.2f}MB -> {new_size/1024:.0f}KB ({reduction:.1f}% reduction)")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def scan_and_compress():
    total_compressed = 0
    total_saved = 0
    
    for folder in IMAGE_FOLDERS:
        if not os.path.exists(folder):
            print(f"Folder not found: {folder}")
            continue
        
        print(f"\nScanning: {folder}")
        print("-" * 40)
        
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(folder, filename)
                original_size = os.path.getsize(filepath)
                
                if original_size >= MIN_SIZE_TO_COMPRESS:
                    print(f"\nProcessing: {filename}")
                    if compress_image(filepath):
                        new_size = os.path.getsize(filepath)
                        total_compressed += 1
                        total_saved += (original_size - new_size)
    
    print("\n" + "=" * 40)
    print(f"Total images compressed: {total_compressed}")
    print(f"Total space saved: {total_saved/1024/1024:.2f}MB")
    print("=" * 40)

if __name__ == '__main__':
    print("=" * 40)
    print("Image Compression Tool")
    print("=" * 40)
    scan_and_compress()
    print("\nDone! Restart the server to see improvements.")
