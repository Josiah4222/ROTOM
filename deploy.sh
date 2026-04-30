#!/bin/bash

# Deployment script for ROTOM Ethiopia Django project
# Run this script on your server after initial setup

set -e  # Exit on error

echo "Starting deployment..."

# Navigate to project directory
cd /var/www/rotom

# Activate virtual environment
source venv/bin/activate

# Pull latest code (if using git)
# git pull origin main

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create cache table if not exists
echo "Creating cache table..."
python manage.py createcachetable

# Restart Gunicorn
echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

# Check service status
echo "Checking service status..."
sudo systemctl status gunicorn --no-pager
sudo systemctl status nginx --no-pager

echo "Deployment completed successfully!"
echo "Visit http://178.104.213.200 to check your site"
