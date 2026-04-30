#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import PreviousEvent

# Clear existing previous events to start fresh
PreviousEvent.objects.all().delete()

# Available images from media/event_images/
available_images = [
    'event_images/_MG_0365.jpg',
    'event_images/24_2.jpg', 
    'event_images/30.jpg',
    'event_images/and7.JPG',
    'event_images/event.jpg',
    'event_images/feeding.png',
    'event_images/IMG_9225.JPG',
    'event_images/IMG_9226.JPG',
    'event_images/IMGL0834.JPG',
    'event_images/OCIAL_MEDIO-108_2.jpg',
    'event_images/previous_event.jpg',
    'event_images/previous_event1.jpg',
    'event_images/previous_event2.jpg',
    'event_images/previous_event3.jpg',
]

# Event data with meaningful titles and descriptions
events_data = [
    {
        'title': 'Annual Elders Day Celebration 2024',
        'description': 'A heartwarming celebration honoring our beloved elders with traditional music, dance, and a special feast. Over 150 seniors joined us for this memorable day filled with joy, laughter, and community spirit.',
        'image': 'event_images/previous_event.jpg'
    },
    {
        'title': 'Community Feeding Program Launch',
        'description': 'The official launch of our expanded feeding program, providing nutritious meals to 200+ elderly community members. Local leaders and volunteers came together to support this vital initiative.',
        'image': 'event_images/feeding.png'
    },
    {
        'title': 'Home Renovation Project Completion',
        'description': 'Celebrating the completion of home renovations for 25 elderly residents, transforming their living spaces into safe, comfortable homes. Volunteers worked tirelessly to make this dream a reality.',
        'image': 'event_images/30.jpg'
    },
    {
        'title': 'Volunteer Appreciation Ceremony',
        'description': 'Honoring our dedicated volunteers who have given countless hours to serve Ethiopia\'s elderly community. Over 100 volunteers were recognized for their outstanding service and commitment.',
        'image': 'event_images/OCIAL_MEDIO-108_2.jpg'
    },
    {
        'title': 'Medical Outreach Program',
        'description': 'Free health checkups and medical consultations for 300+ seniors in rural communities. Medical professionals volunteered their time to provide essential healthcare services.',
        'image': 'event_images/IMG_9225.JPG'
    },
    {
        'title': 'Traditional Coffee Ceremony',
        'description': 'A beautiful traditional Ethiopian coffee ceremony bringing together elders and youth to share stories, wisdom, and cultural traditions. A celebration of our rich heritage and intergenerational bonds.',
        'image': 'event_images/and7.JPG'
    },
    {
        'title': 'Winter Clothing Distribution',
        'description': 'Distribution of warm clothing and blankets to 400+ elderly residents during the cold season. Community donations made it possible to keep our elders warm and comfortable.',
        'image': 'event_images/24_2.jpg'
    },
    {
        'title': 'Holiday Program With the City Mayor',
        'description': 'A special holiday program organized in collaboration with the city mayor, bringing joy and celebration to our elderly community members.',
        'image': 'event_images/event.jpg'
    },
    {
        'title': 'Literacy Program Graduation',
        'description': 'Celebrating the graduation of elderly participants from our adult literacy program.',
        'image': 'event_images/previous_event3.jpg'
    },
    {
        'title': 'Rotom Ethiopia was visited by the previous mayor of the City',
        'description': 'An honourable visit by the previous city mayor to our center, recognizing our work with the elderly community.',
        'image': 'event_images/previous_event2.jpg'
    },
    {
        'title': 'Seniors Dancing and having fun during the holiday',
        'description': 'A joyful holiday celebration where our seniors danced, laughed, and enjoyed quality time together.',
        'image': 'event_images/previous_event.jpg'
    },
    {
        'title': 'Gifts were given during Christmas',
        'description': 'Spreading Christmas joy by distributing gifts to our beloved elderly community members.',
        'image': 'event_images/previous_event1.jpg'
    },
    {
        'title': 'Celebrating Meskel With our beloved volunteers',
        'description': 'A warm Meskel celebration shared with our dedicated volunteers who make our mission possible.',
        'image': 'event_images/OCIAL_MEDIO-108_2.jpg'
    },
]

# Create events with dates spread over the past 2 years
base_date = datetime.now() - timedelta(days=730)  # 2 years ago

print("Creating past events with images...")

for i, event_data in enumerate(events_data):
    # Create event date (spread events over past 2 years)
    event_date = base_date + timedelta(days=i * 50 + random.randint(0, 30))
    
    previous_event = PreviousEvent.objects.create(
        title=event_data['title'],
        description=event_data['description'],
        event_date=event_date,
        image=event_data['image']
    )
    
    print(f"Created: {previous_event.title} - {previous_event.event_date.strftime('%Y-%m-%d')}")

print(f"\nSuccessfully created {len(events_data)} past events!")
print("All events now have images and detailed descriptions.")