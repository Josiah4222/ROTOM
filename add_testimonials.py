#!/usr/bin/env python
"""
Script to add existing static testimonials to the database
Run with: python add_testimonials.py
"""

import os
import django
import shutil
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import Testimonial

def add_testimonials():
    """Add existing static testimonials to the database"""
    
    testimonials_data = [
        {
            'name': 'Senior Tsige',
            'role': 'Program Beneficiary',
            'quote': "My children thank you so much. You've given me the privilege to see the outside. I haven't seen the outside in over 30 years. You give me an opportunity to chat with people and see the outside.",
            'image_path': 'static/images/tsige niguse.PNG',
            'order': 0,
            'is_active': True
        },
        {
            'name': 'Senior Adanech Tafese',
            'role': 'Program Beneficiary',
            'quote': "The care and support I receive from ROTOM Ethiopia has given me a new lease on life. I feel valued, respected, and part of a loving community.",
            'image_path': 'static/images/adanech.PNG',
            'order': 1,
            'is_active': True
        },
        {
            'name': 'Ato Fasikaw Mola',
            'role': 'Deputy Director General, Civil Society Organizations Authority',
            'quote': "We are truly impressed by the remarkable work being done at Rotom Ethiopia. The dignity, cleanliness, and quality of care provided to the elderly are exceptional and set a powerful example for others. Your commitment to compassionate service and the involvement of dedicated volunteers is inspiring. We sincerely appreciate your efforts and proudly stand in support of your mission.",
            'image_path': 'static/images/fasikaw.jpg',
            'order': 2,
            'is_active': True
        }
    ]
    
    print("Adding testimonials to database...\n")
    
    for data in testimonials_data:
        # Check if testimonial already exists
        existing = Testimonial.objects.filter(name=data['name']).first()
        
        if existing:
            print(f"⚠️  Testimonial for '{data['name']}' already exists. Skipping...")
            continue
        
        # Create testimonial
        testimonial = Testimonial(
            name=data['name'],
            role=data['role'],
            quote=data['quote'],
            order=data['order'],
            is_active=data['is_active']
        )
        
        # Copy image to media folder if it exists
        source_path = Path(data['image_path'])
        if source_path.exists():
            # Create media/testimonials directory if it doesn't exist
            media_dir = Path('media/testimonials')
            media_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy image to media folder
            dest_filename = source_path.name
            dest_path = media_dir / dest_filename
            shutil.copy2(source_path, dest_path)
            
            # Set the image field (relative to MEDIA_ROOT)
            testimonial.image = f'testimonials/{dest_filename}'
            print(f"✅ Added '{data['name']}' with image")
        else:
            print(f"⚠️  Image not found for '{data['name']}' at {source_path}")
            print(f"✅ Added '{data['name']}' without image")
        
        testimonial.save()
    
    print(f"\n✅ Done! Total testimonials in database: {Testimonial.objects.count()}")
    print("\nYou can now view them at: http://localhost:8000/dashboard/manage-testimonials/")

if __name__ == '__main__':
    add_testimonials()
