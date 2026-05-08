#!/usr/bin/env python
"""
Script to migrate existing partner logos to the database.
Run this once to add your current partners to the new system.
"""
import os
import django
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import Partner
from django.core.files import File

# List of existing partners with their image files
EXISTING_PARTNERS = [
    {'name': 'HFT Foundation', 'file': 'static/images/HFTFrec_tan.png'},
    {'name': 'Holland Foundation', 'file': 'static/images/holland.png'},
    {'name': 'ROTOM USA', 'file': 'static/images/rotom_usa.jpg'},
    {'name': 'Canada Partnership', 'file': 'static/images/canada.jpg'},
    {'name': 'GK Organization', 'file': 'static/images/gk.jpg'},
    {'name': 'AHSAM', 'file': 'static/images/ahsam.jpg'},
    {'name': 'Andu Foundation', 'file': 'static/images/andu.jpg'},
    {'name': 'Alfa Organization', 'file': 'static/images/alfa.jpg'},
    {'name': 'Beautiful World', 'file': 'static/images/beautifulworld.jpg'},
    {'name': 'EDF', 'file': 'static/images/edf.jpg'},
    {'name': 'Global Care', 'file': 'static/images/globalcare.jpg'},
    {'name': 'Maranatha', 'file': 'static/images/maranatha.jpg'},
    {'name': 'Pyramid Foundation', 'file': 'static/images/pyramid.jpg'},
]

def migrate_partners():
    print("Starting partner migration...\n")
    
    added_count = 0
    skipped_count = 0
    error_count = 0
    
    for index, partner_data in enumerate(EXISTING_PARTNERS, start=1):
        name = partner_data['name']
        file_path = partner_data['file']
        
        # Check if partner already exists
        if Partner.objects.filter(name=name).exists():
            print(f"⊘ Skipped: {name} (already exists)")
            skipped_count += 1
            continue
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"✗ Error: {name} - File not found: {file_path}")
            error_count += 1
            continue
        
        try:
            # Create partner entry
            partner = Partner(
                name=name,
                order=index * 10,  # 10, 20, 30, etc. for easy reordering
                is_active=True
            )
            
            # Copy the file to media/partners/
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                partner.logo.save(filename, File(f), save=True)
            
            print(f"✓ Added: {name}")
            added_count += 1
            
        except Exception as e:
            print(f"✗ Error: {name} - {str(e)}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"Migration Complete!")
    print(f"{'='*50}")
    print(f"✓ Added: {added_count}")
    print(f"⊘ Skipped: {skipped_count}")
    print(f"✗ Errors: {error_count}")
    print(f"{'='*50}")
    
    if added_count > 0:
        print(f"\nYou can now manage partners from the admin dashboard at:")
        print(f"  /admin/rotom/partner/")
        print(f"\nTo add/edit/delete partners:")
        print(f"  1. Go to the admin dashboard")
        print(f"  2. Click 'Partners' in the ROTOM section")
        print(f"  3. Add new partners or edit existing ones")

if __name__ == '__main__':
    migrate_partners()
