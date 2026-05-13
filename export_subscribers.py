#!/usr/bin/env python
"""
Export Subscribers to CSV
Run this to get a list of all email subscribers.
"""
import os
import csv
from datetime import datetime
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import Subscriber

def export_subscribers():
    print("=" * 60)
    print("Exporting Subscribers")
    print("=" * 60)
    
    # Get all subscribers
    subscribers = Subscriber.objects.all().order_by('-subscribed_at')
    total = subscribers.count()
    
    print(f"Total subscribers: {total}")
    
    if total == 0:
        print("\n⚠️  No subscribers found in the database.")
        return
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'subscribers_{timestamp}.csv'
    
    # Export to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Email', 'Subscribed Date', 'Subscribed Time'])
        
        # Write subscriber data
        for subscriber in subscribers:
            writer.writerow([
                subscriber.email,
                subscriber.subscribed_at.strftime('%Y-%m-%d'),
                subscriber.subscribed_at.strftime('%H:%M:%S')
            ])
    
    print(f"\n✅ SUCCESS! Subscribers exported to: {filename}")
    print("\nSubscriber List:")
    print("-" * 60)
    
    for i, subscriber in enumerate(subscribers, 1):
        print(f"{i}. {subscriber.email} (subscribed: {subscriber.subscribed_at.strftime('%Y-%m-%d %H:%M')})")
    
    print("-" * 60)
    print(f"\nYou can now:")
    print(f"1. Open {filename} in Excel or Google Sheets")
    print(f"2. Copy the email addresses")
    print(f"3. Use them for manual email campaigns")
    print(f"4. Import into Mailchimp, SendGrid, or other email services")

if __name__ == '__main__':
    export_subscribers()
