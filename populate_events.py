"""
Script to populate sample events for testing
Run: python manage.py shell < populate_events.py
Or: python populate_events.py (with Django setup)
"""
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import Event, PreviousEvent

# Clear existing events (optional - comment out if you want to keep existing)
print("Clearing existing events...")
Event.objects.all().delete()
PreviousEvent.objects.all().delete()

# Source images from static folder
SOURCE_IMAGES = [
    'rotom/static/images/champions.JPG',
    'rotom/static/images/centerbased.jpg',
    'rotom/static/images/homebased.jpg',
    'rotom/static/images/volunteers_group.JPG',
    'rotom/static/images/gather.jpg',
    'rotom/static/images/newcenter.jpg',
    'rotom/static/images/graduates.jpg',
    'rotom/static/images/volun.jpg',
]

# Ensure media/event_images directory exists
os.makedirs('media/event_images', exist_ok=True)

def copy_image_to_media(source_path, new_name):
    """Copy image from static to media folder"""
    if os.path.exists(source_path):
        dest_path = f'media/event_images/{new_name}'
        shutil.copy2(source_path, dest_path)
        return f'event_images/{new_name}'
    return None

# Create Upcoming Events
print("\nCreating upcoming events...")

upcoming_events_data = [
    {
        'title': 'Annual Senior Appreciation Day',
        'description': 'Join us for our annual celebration honoring the seniors in our community. There will be music, food, and heartfelt moments as we recognize the wisdom and contributions of our elders. Family members and volunteers are welcome to attend.',
        'days_from_now': 14,
        'image_source': SOURCE_IMAGES[0],
        'image_name': 'senior_appreciation.jpg'
    },
    {
        'title': 'Volunteer Training Workshop',
        'description': 'A comprehensive training session for new and existing volunteers. Learn about elderly care best practices, communication techniques, and how to make a meaningful impact in the lives of seniors. Lunch will be provided.',
        'days_from_now': 21,
        'image_source': SOURCE_IMAGES[3],
        'image_name': 'volunteer_training.jpg'
    },
    {
        'title': 'Community Health Screening',
        'description': 'Free health screening event for seniors in the Bishoftu area. Services include blood pressure checks, diabetes screening, vision tests, and consultations with healthcare professionals. Transportation available upon request.',
        'days_from_now': 30,
        'image_source': SOURCE_IMAGES[1],
        'image_name': 'health_screening.jpg'
    },
]

for event_data in upcoming_events_data:
    image_path = copy_image_to_media(event_data['image_source'], event_data['image_name'])
    if image_path:
        event = Event.objects.create(
            title=event_data['title'],
            description=event_data['description'],
            event_date=timezone.now() + timedelta(days=event_data['days_from_now']),
            image=image_path
        )
        print(f"  Created: {event.title}")
    else:
        print(f"  Skipped (no image): {event_data['title']}")

# Create Previous Events (Gallery)
print("\nCreating previous events gallery...")

previous_events_data = [
    {
        'title': 'Christmas Celebration 2024',
        'description': 'A joyful Christmas celebration with our seniors, featuring traditional Ethiopian food, music, and gift-giving.',
        'days_ago': 10,
        'image_source': SOURCE_IMAGES[4],
        'image_name': 'christmas_2024.jpg'
    },
    {
        'title': 'New Center Opening',
        'description': 'The grand opening of our new care center in Bishoftu, providing a home for seniors in need.',
        'days_ago': 45,
        'image_source': SOURCE_IMAGES[5],
        'image_name': 'center_opening.jpg'
    },
    {
        'title': 'Graduation Ceremony',
        'description': 'Celebrating the educational achievements of grandchildren supported by ROTOM Ethiopia.',
        'days_ago': 60,
        'image_source': SOURCE_IMAGES[6],
        'image_name': 'graduation.jpg'
    },
    {
        'title': 'Volunteer Appreciation Event',
        'description': 'Honoring our dedicated volunteers who give their time and love to support our seniors.',
        'days_ago': 90,
        'image_source': SOURCE_IMAGES[7],
        'image_name': 'volunteer_appreciation.jpg'
    },
    {
        'title': 'Home Visit Program',
        'description': 'Our team visiting seniors in their homes, providing care packages and companionship.',
        'days_ago': 120,
        'image_source': SOURCE_IMAGES[2],
        'image_name': 'home_visit.jpg'
    },
    {
        'title': 'Community Outreach Day',
        'description': 'Reaching out to the community to raise awareness about elderly care and support.',
        'days_ago': 150,
        'image_source': SOURCE_IMAGES[0],
        'image_name': 'outreach_day.jpg'
    },
    {
        'title': 'Senior Health Workshop',
        'description': 'Educational workshop on health and wellness for seniors and their caregivers.',
        'days_ago': 180,
        'image_source': SOURCE_IMAGES[1],
        'image_name': 'health_workshop.jpg'
    },
    {
        'title': 'Cultural Day Celebration',
        'description': 'Celebrating Ethiopian culture and traditions with our seniors through music, dance, and storytelling.',
        'days_ago': 200,
        'image_source': SOURCE_IMAGES[3],
        'image_name': 'cultural_day.jpg'
    },
]

for event_data in previous_events_data:
    image_path = copy_image_to_media(event_data['image_source'], event_data['image_name'])
    if image_path:
        event = PreviousEvent.objects.create(
            title=event_data['title'],
            description=event_data['description'],
            event_date=timezone.now() - timedelta(days=event_data['days_ago']),
            image=image_path
        )
        print(f"  Created: {event.title}")
    else:
        print(f"  Skipped (no image): {event_data['title']}")

print("\n" + "="*50)
print(f"Created {Event.objects.count()} upcoming events")
print(f"Created {PreviousEvent.objects.count()} previous events")
print("="*50)
print("\nDone! Visit /events/ to see the events.")
