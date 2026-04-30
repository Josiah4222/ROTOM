#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import InterestCategory

interests = [
    # Direct Care
    "Elder Companionship",
    "Personal Care Assistance",
    "Home Visits",
    # Health & Wellness
    "Medical Support",
    "Physical Therapy Assistance",
    "Mental Health & Counseling Support",
    # Practical Support
    "Home Renovation & Repairs",
    "Cooking & Meal Preparation",
    "Cleaning & Housekeeping",
    "Transportation & Errands",
    # Programs & Activities
    "Arts & Crafts",
    "Music & Entertainment",
    "Spiritual Support & Prayer",
    "Exercise & Recreation",
    # Community & Outreach
    "Fundraising & Events",
    "Community Awareness Campaigns",
    "Social Media & Content Creation",
    "Photography & Videography",
    # Admin & Professional
    "Office Work",
    "Translation & Language Support",
    "Teaching & Literacy Support",
    "IT & Tech Support",
]

created, skipped = 0, 0
for name in interests:
    obj, was_created = InterestCategory.objects.get_or_create(name=name)
    if was_created:
        created += 1
        print(f"  Added: {name}")
    else:
        skipped += 1
        print(f"  Exists: {name}")

print(f"\nDone. {created} added, {skipped} already existed.")
