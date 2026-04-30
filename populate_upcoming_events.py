#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import Event
from django.utils import timezone

# Clear existing upcoming events to start fresh
Event.objects.filter(event_date__gte=timezone.now()).delete()

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
]

# Upcoming events data
upcoming_events_data = [
    {
        'title': 'Spring Health Fair 2026',
        'description': 'Join us for a comprehensive health fair featuring free medical checkups, health screenings, and wellness consultations for seniors. Medical professionals will provide blood pressure checks, diabetes screening, eye exams, and health education sessions. Light refreshments and health information packets will be provided.',
        'image': 'event_images/IMG_9225.JPG',
        'days_from_now': 15
    },
    {
        'title': 'Intergenerational Storytelling Festival',
        'description': 'A beautiful celebration where elders share their life stories, wisdom, and cultural traditions with younger generations. This event will feature traditional Ethiopian storytelling, folk tales, and personal narratives that preserve our rich heritage. Participants will enjoy traditional coffee and snacks.',
        'image': 'event_images/and7.JPG',
        'days_from_now': 28
    },
    {
        'title': 'Community Garden Planting Day',
        'description': 'Help us expand our community garden project! Volunteers and seniors will work together to plant vegetables, herbs, and flowers that will provide fresh produce for our feeding programs. All tools and materials will be provided. This is a great opportunity for physical activity and community bonding.',
        'image': 'event_images/IMGL0834.JPG',
        'days_from_now': 42
    },
    {
        'title': 'Annual Volunteer Recognition Ceremony',
        'description': 'Celebrating our amazing volunteers who dedicate their time and hearts to serving Ethiopia\'s elderly community. This special ceremony will honor outstanding volunteers, share success stories, and welcome new volunteers to our mission. Awards, certificates, and a special dinner will be provided.',
        'image': 'event_images/OCIAL_MEDIO-108_2.jpg',
        'days_from_now': 56
    },
    {
        'title': 'Summer Skills Workshop Series',
        'description': 'A month-long series of workshops teaching traditional Ethiopian crafts, modern life skills, and income-generating activities. Seniors will learn pottery, weaving, basic computer skills, and small business management. All materials included, and participants will take home their creations.',
        'image': 'event_images/IMG_9226.JPG',
        'days_from_now': 70
    }
]

print("Creating upcoming events...")

for event_data in upcoming_events_data:
    # Create event date in the future
    event_date = timezone.now() + timedelta(days=event_data['days_from_now'])
    
    event = Event.objects.create(
        title=event_data['title'],
        description=event_data['description'],
        event_date=event_date,
        image=event_data['image']
    )
    
    print(f"Created: {event.title} - {event.event_date.strftime('%Y-%m-%d %H:%M')}")

print(f"\nSuccessfully created {len(upcoming_events_data)} upcoming events!")
print("All events have images and detailed descriptions.")