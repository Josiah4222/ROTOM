# Django Deployment Guide for Ubuntu 22.04 Server (SQLite Version)

**Server Details:**
- Hostname: rotomEthiopia
- IP: 178.104.213.200
- OS: Ubuntu 22.04
- Location: Falkenstein

## Prerequisites on Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip nginx redis-server git -y

# Install system dependencies for Pillow
sudo apt install libjpeg-dev zlib1g-dev -y
```

## 1. Setup Project Directory

```bash
# Create project directory
sudo mkdir -p /var/www/rotom
sudo chown $USER:$USER /var/www/rotom
cd /var/www/rotom

# Clone or upload your project
# If using git:
git clone <your-repo-url> .

# Or upload files via SCP from your local machine:
# scp -r /path/to/ROTOM/* root@178.104.213.200:/var/www/rotom/
```

## 2. Setup Python Virtual Environment

```bash
cd /var/www/rotom
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Environment Variables

Create `.env` file in `/var/www/rotom/`:

```bash
nano .env
```

Add the following (update with your actual values):

```env
SECRET_KEY=your-very-secure-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=178.104.213.200,rotomethiopia.org,www.rotomethiopia.org

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=rotomethiopia@reachone-touchone.org
EMAIL_HOST_PASSWORD=your_app_password_here
DEFAULT_FROM_EMAIL=ROTOM Ethiopia <rotomethiopia@reachone-touchone.org>

# Payment
CHAPA_SECRET_KEY=CHASECK-O6jk9SKQlZJcn8d9qib00WLbvzcRJreo
PAYPAL_RECEIVER_EMAIL=test@example.com
PAYPAL_TEST=False
```

## 4. Run Django Setup Commands

```bash
cd /var/www/rotom
source venv/bin/activate

# Create cache table
python manage.py createcachetable

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Set proper permissions for SQLite database
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3
sudo chown www-data:www-data /var/www/rotom
```

## 5. Setup Gunicorn

Create systemd service file:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

## 6. Setup Nginx

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/rotom
```

## 7. Enable and Start Services

```bash
# Enable and start Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/rotom /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 8. SSL Certificate (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (after domain is pointed to server)
sudo certbot --nginx -d rotomethiopia.org -d www.rotomethiopia.org
```

## Maintenance Commands

```bash
# View Gunicorn logs
sudo journalctl -u gunicorn -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Restart services after code changes
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Update code
cd /var/www/rotom
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## Important: SQLite Database Backup

Since you're using SQLite, regular backups are crucial:

```bash
# Manual backup
cp db.sqlite3 db.sqlite3.backup

# Automated backup (see backup.sh script)
chmod +x backup.sh
sudo crontab -e
# Add: 0 2 * * * /var/www/rotom/backup.sh
```

## Security Checklist

- [ ] Change default SSH port
- [ ] Disable root SSH login
- [ ] Setup SSH key authentication
- [ ] Configure firewall (UFW)
- [ ] Setup fail2ban
- [ ] Regular backups of SQLite database
- [ ] Keep system updated
- [ ] Monitor logs regularly

## SQLite Considerations

**Advantages:**
- Simple setup, no database server needed
- Perfect for small to medium traffic sites
- Easy backups (just copy the file)

**Limitations:**
- Not ideal for high concurrent writes
- File-based, so ensure proper permissions
- Regular backups are essential

For your use case (NGO website), SQLite should work perfectly fine!
