#!/usr/bin/env python
"""
Test Email Configuration
Run this to verify your email settings work correctly.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("=" * 50)
    print("Testing Email Configuration")
    print("=" * 50)
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Email User: {settings.EMAIL_HOST_USER}")
    print(f"Email Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 50)
    
    try:
        print("\nSending test email...")
        send_mail(
            subject='Test Email from ROTOM Ethiopia',
            message='This is a test email to verify your email configuration is working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to yourself
            fail_silently=False,
        )
        print("✅ SUCCESS! Email sent successfully!")
        print(f"Check your inbox at: {settings.EMAIL_HOST_USER}")
        return True
    except Exception as e:
        print("❌ FAILED! Email could not be sent.")
        print(f"Error: {str(e)}")
        print("\nPossible solutions:")
        print("1. If using Gmail, generate an App Password:")
        print("   https://myaccount.google.com/apppasswords")
        print("2. Enable 2-Factor Authentication first")
        print("3. Or enable 'Less secure app access' (not recommended):")
        print("   https://myaccount.google.com/lesssecureapps")
        return False

if __name__ == '__main__':
    test_email()
