#!/usr/bin/env python
"""
Performance optimization script for ROTOM Ethiopia Django project.
Run this after making the code changes to set up database optimizations.
"""

import os
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

def create_cache_table():
    """Create database cache table for better caching performance."""
    print("Creating database cache table...")
    execute_from_command_line(['manage.py', 'createcachetable'])

def create_migrations():
    """Create migrations for the model changes."""
    print("Creating migrations for model changes...")
    execute_from_command_line(['manage.py', 'makemigrations'])

def apply_migrations():
    """Apply the migrations."""
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

def collect_static():
    """Collect static files for production."""
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

def main():
    """Run all optimization steps."""
    print("🚀 Starting ROTOM Performance Optimization...")
    
    try:
        create_migrations()
        apply_migrations()
        create_cache_table()
        collect_static()
        
        print("\n✅ Performance optimization completed successfully!")
        print("\n📋 Next steps for production deployment:")
        print("1. Switch to PostgreSQL database")
        print("2. Set up Redis for caching")
        print("3. Configure CDN for static/media files")
        print("4. Set up Celery for async tasks")
        print("5. Add monitoring with Sentry")
        
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())