#!/usr/bin/env python
"""
Script to add the current pattern_green.png to the database as the active pattern.
Run this once to migrate your existing pattern to the new system.
"""
import os
import django
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import NavbarPattern
from django.core.files import File

def add_current_pattern():
    # Check if pattern already exists
    if NavbarPattern.objects.filter(name="Green Ethiopian Pattern").exists():
        print("Pattern already exists in database!")
        return
    
    # Path to the current pattern
    pattern_path = 'static/images/pattern_green.png'
    
    if not os.path.exists(pattern_path):
        print(f"Error: Pattern file not found at {pattern_path}")
        return
    
    # Create the pattern entry
    pattern = NavbarPattern(
        name="Green Ethiopian Pattern",
        height=60,
        opacity=0.80,
        is_active=True
    )
    
    # Copy the file to media/patterns/
    with open(pattern_path, 'rb') as f:
        pattern.image.save('pattern_green.png', File(f), save=True)
    
    print(f"✓ Successfully added '{pattern.name}' to the database!")
    print(f"  - Height: {pattern.height}px")
    print(f"  - Opacity: {pattern.opacity}")
    print(f"  - Active: {pattern.is_active}")
    print(f"\nYou can now manage patterns from the admin dashboard at:")
    print(f"  /admin/rotom/navbarpattern/")

if __name__ == '__main__':
    add_current_pattern()
