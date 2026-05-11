"""
Compress all images in the project for faster loading.
Run: python compress_images.py
"""
from PIL import Image, ImageOps
import os
import io

IMAGE_FOLDERS = [
    'static/images',
    'rotom/static/images',
    'media/event_images',
    'event_images',
]

ROOT_IMAGES = [
    'banner rotom.png',
]

MAX_SIZE = 1920
JPEG_QUALITY = 80
WEBP_QUALITY = 80
MIN_SIZE_TO_COMPRESS = 10 * 1024  # 10KB - compress almost everything

def get_size_str(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f}KB"
    else:
        return f"{size_bytes/1024/1024:.2f}MB"

def optimize_image(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        return False

    original_size = os.path.getsize(filepath)
    if original_size < MIN_SIZE_TO_COMPRESS:
        return False

    try:
        with Image.open(filepath) as img:
            img.load()
    except Exception as e:
        print(f"  Error opening: {e}")
        return False

    original_mode = img.mode

    needs_recompress = False
    ratio = 1.0

    w, h = img.size
    if w > MAX_SIZE or h > MAX_SIZE:
        ratio = min(MAX_SIZE / w, MAX_SIZE / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        needs_recompress = True
        print(f"  Resized: {w}x{h} -> {new_w}x{new_h}")

    if ext in ('.jpg', '.jpeg'):
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=True)
        new_size = buf.tell()
        if new_size < original_size:
            with open(filepath, 'wb') as f:
                f.write(buf.getvalue())
            print(f"  JPEG: {get_size_str(original_size)} -> {get_size_str(new_size)} ({((original_size-new_size)/original_size)*100:.0f}% saved)")
            return True
        else:
            return False

    elif ext == '.png':
        if img.mode == 'P':
            img = img.convert('RGBA')
        buf = io.BytesIO()
        img.save(buf, 'PNG', optimize=True)
        new_size = buf.tell()
        if new_size < original_size:
            with open(filepath, 'wb') as f:
                f.write(buf.getvalue())
            print(f"  PNG: {get_size_str(original_size)} -> {get_size_str(new_size)} ({((original_size-new_size)/original_size)*100:.0f}% saved)")
            return True
        else:
            return False

    elif ext == '.gif':
        buf = io.BytesIO()
        img.save(buf, 'GIF', optimize=True)
        new_size = buf.tell()
        if new_size < original_size:
            with open(filepath, 'wb') as f:
                f.write(buf.getvalue())
            print(f"  GIF: {get_size_str(original_size)} -> {get_size_str(new_size)} ({((original_size-new_size)/original_size)*100:.0f}% saved)")
            return True
        return False

    elif ext == '.webp':
        buf = io.BytesIO()
        img.save(buf, 'WEBP', quality=WEBP_QUALITY)
        new_size = buf.tell()
        if new_size < original_size:
            with open(filepath, 'wb') as f:
                f.write(buf.getvalue())
            print(f"  WebP: {get_size_str(original_size)} -> {get_size_str(new_size)} ({((original_size-new_size)/original_size)*100:.0f}% saved)")
            return True
        return False

    return False

def scan_and_compress():
    total_compressed = 0
    total_original = 0
    total_final = 0

    all_paths = []
    for folder in IMAGE_FOLDERS:
        if not os.path.exists(folder):
            print(f"Folder not found: {folder}")
            continue
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath) and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                all_paths.append(filepath)

    for filepath in ROOT_IMAGES:
        if os.path.exists(filepath):
            all_paths.append(filepath)

    for filepath in sorted(all_paths):
        size = os.path.getsize(filepath)
        total_original += size
        print(f"\n{filepath} ({get_size_str(size)})")
        if optimize_image(filepath):
            total_compressed += 1
        new_size = os.path.getsize(filepath)
        total_final += new_size

    print("\n" + "=" * 50)
    print(f"Images processed: {len(all_paths)}")
    print(f"Images compressed: {total_compressed}")
    print(f"Total: {get_size_str(total_original)} -> {get_size_str(total_final)} ({((total_original-total_final)/total_original)*100:.0f}% saved)")
    print("=" * 50)

if __name__ == '__main__':
    print("=" * 50)
    print("Image Compression Tool")
    print("=" * 50)
    scan_and_compress()
    print("\nDone!")
