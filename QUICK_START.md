# Quick Start Deployment Guide (SQLite Version)

## Step 1: Connect to Your Server

```bash
ssh root@178.104.213.200
```

## Step 2: Run Initial Setup

```bash
# Update system
apt update && apt upgrade -y

# Install required packages (no PostgreSQL needed!)
apt install python3.11 python3.11-venv python3-pip nginx redis-server git libjpeg-dev zlib1g-dev -y

# Create project directory
mkdir -p /var/www/rotom
cd /var/www/rotom
```

## Step 3: Upload Your Project

From your local machine:

```bash
# Compress your project (exclude venv, __pycache__, etc.)
tar -czf rotom.tar.gz --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' .

# Upload to server
scp rotom.tar.gz root@178.104.213.200:/var/www/rotom/

# On server, extract
cd /var/www/rotom
tar -xzf rotom.tar.gz
rm rotom.tar.gz
```

## Step 4: Setup Python Environment

```bash
cd /var/www/rotom
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 5: Configure Environment

```bash
nano .env
```

Update with:
```env
SECRET_KEY=generate-a-new-secret-key-here-use-django-secret-key-generator
DEBUG=False
ALLOWED_HOSTS=178.104.213.200,rotomethiopia.org,www.rotomethiopia.org

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=rotomethiopia@reachone-touchone.org
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=ROTOM Ethiopia <rotomethiopia@reachone-touchone.org>

CHAPA_SECRET_KEY=CHASECK-O6jk9SKQlZJcn8d9qib00WLbvzcRJreo
PAYPAL_RECEIVER_EMAIL=test@example.com
PAYPAL_TEST=False
```

## Step 6: Run Django Commands

```bash
source venv/bin/activate
python manage.py createcachetable
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# IMPORTANT: Set proper permissions for SQLite database
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3
sudo chown www-data:www-data /var/www/rotom
```

## Step 7: Setup Gunicorn Service

```bash
# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn

# Copy service file
sudo cp gunicorn.service /etc/systemd/system/

# Start service
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

## Step 8: Setup Nginx

```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/rotom

# Enable site
sudo ln -s /etc/nginx/sites-available/rotom /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## Step 9: Configure Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Step 10: Test Your Site

Visit: http://178.104.213.200

## Troubleshooting

### Check Gunicorn logs:
```bash
sudo journalctl -u gunicorn -f
```

### Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/rotom_error.log
```

### Restart services:
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Fix SQLite permissions (if you get database errors):
```bash
cd /var/www/rotom
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3
sudo chown www-data:www-data .
```

## After Domain Setup

Once you point your domain to 178.104.213.200:

```bash
# Install SSL certificate
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d rotomethiopia.org -d www.rotomethiopia.org

# Update .env to enable SSL settings
# Then restart services
```

## Regular Maintenance

```bash
# Make scripts executable
chmod +x deploy.sh backup.sh

# Run deployment script for updates
./deploy.sh

# Setup automated backups
sudo crontab -e
# Add: 0 2 * * * /var/www/rotom/backup.sh

# Manual database backup
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d)
```

## SQLite Tips

- Always backup before updates: `cp db.sqlite3 db.sqlite3.backup`
- Check database size: `ls -lh db.sqlite3`
- Optimize database: `python manage.py dbshell` then `VACUUM;`
- Monitor disk space: `df -h`
