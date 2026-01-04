#!/bin/bash

# ROTOM Ethiopia VPS Deployment Script
echo "🚀 Starting ROTOM Ethiopia deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git curl

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /var/www/rotom
sudo chown $USER:$USER /var/www/rotom
cd /var/www/rotom

# Clone or copy your project (adjust as needed)
# git clone your_repository_url .

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create PostgreSQL database and user
echo "🗄️ Setting up PostgreSQL database..."
sudo -u postgres psql << EOF
CREATE DATABASE rotom_db;
CREATE USER rotom_user WITH PASSWORD 'your_secure_password';
ALTER ROLE rotom_user SET client_encoding TO 'utf8';
ALTER ROLE rotom_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE rotom_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE rotom_db TO rotom_user;
\q
EOF

# Run Django migrations
echo "🔄 Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create cache table
echo "💾 Creating cache table..."
python manage.py createcachetable

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional - you can do this manually later)
echo "👤 Create superuser manually after deployment with: python manage.py createsuperuser"

echo "✅ Deployment script completed!"
echo "📝 Next steps:"
echo "1. Update your .env file with correct values"
echo "2. Configure Nginx"
echo "3. Set up Gunicorn service"
echo "4. Configure SSL certificate"