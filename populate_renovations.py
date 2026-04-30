#!/usr/bin/env python
import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import HouseRenovation
from django.conf import settings

renovations_data = [
    {
        'name': "Jemanesh's Home",
        'description': "Jemanesh's home transformed with sturdy roofing, reinforced walls, and a safer, more comfortable living environment.",
        'before': 'rotom/static/images/jemanesh.jpg',
        'after': 'rotom/static/images/jemaneshafter.jpg',
        'before_dest': 'renovations/jemanesh_before.jpg',
        'after_dest': 'renovations/jemaneshafter.jpg',
    },
    {
        'name': "Senior's Home Renovation",
        'description': "A revitalized home with improved safety, insulation, and comfort, enhancing the senior's quality of life.",
        'before': 'rotom/static/images/before.jpg',
        'after': 'rotom/static/images/after.jpg',
        'before_dest': 'renovations/senior_before.jpg',
        'after_dest': 'renovations/senior_after.jpg',
    },
]

media_root = settings.MEDIA_ROOT
reno_dir = os.path.join(media_root, 'renovations')
os.makedirs(reno_dir, exist_ok=True)

for r in renovations_data:
    # Copy images to media folder
    before_dest = os.path.join(media_root, r['before_dest'])
    after_dest = os.path.join(media_root, r['after_dest'])

    if not os.path.exists(before_dest):
        shutil.copy2(r['before'], before_dest)
        print(f"  Copied: {r['before']} -> {before_dest}")

    if not os.path.exists(after_dest):
        shutil.copy2(r['after'], after_dest)
        print(f"  Copied: {r['after']} -> {after_dest}")

    obj, created = HouseRenovation.objects.get_or_create(
        name=r['name'],
        defaults={
            'description': r['description'],
            'before_image': r['before_dest'],
            'after_image': r['after_dest'],
        }
    )
    print(f"  {'Created' if created else 'Already exists'}: {obj.name}")

print(f"\nDone. {HouseRenovation.objects.count()} renovation(s) in database.")
