# Quick Deployment Guide

## 🚀 Fast Deployment (If Already Setup)

If your server is already configured and you just need to update code:

### From Your Local Machine

```bash
# 1. Commit your changes
git add .
git commit -m "Added milestone management system"
git push origin main
```

### On the Server

```bash
# 2. SSH into server
ssh root@178.104.213.200

# 3. Navigate to project
cd /var/www/rotom

# 4. Pull latest changes
git pull origin main

# 5. Run deployment script
chmod +x deploy.sh
./deploy.sh
```

That's it! Your site is updated.

---

## 📋 Manual Deployment Steps

If you prefer to run commands manually:

```bash
# SSH into server
ssh root@178.104.213.200

# Navigate to project
cd /var/www/rotom

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Set permissions
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 🆕 First Time Deployment

If this is your first deployment:

### 1. Prepare Production Environment

```bash
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Create .env.production with:
# - New SECRET_KEY
# - DEBUG=False
# - Production ALLOWED_HOSTS
# - Email credentials
```

### 2. Upload Files

```bash
# Option A: Using Git (Recommended)
ssh root@178.104.213.200
cd /var/www/rotom
git clone <your-repo-url> .

# Option B: Using SCP
scp -r /path/to/ROTOM/* root@178.104.213.200:/var/www/rotom/
```

### 3. Setup on Server

```bash
ssh root@178.104.213.200
cd /var/www/rotom

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy production env
cp .env.production .env

# Run migrations
python manage.py migrate

# Create cache table
python manage.py createcachetable

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Add initial milestones
python add_milestones.py

# Set permissions
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3
sudo chown www-data:www-data /var/www/rotom

# Setup Gunicorn service (if not done)
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Setup Nginx (if not done)
sudo cp nginx.conf /etc/nginx/sites-available/rotom
sudo ln -s /etc/nginx/sites-available/rotom /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## ✅ Verification Checklist

After deployment, verify:

```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Check Nginx status
sudo systemctl status nginx

# View Gunicorn logs
sudo journalctl -u gunicorn -f

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

Visit your website and test:
- [ ] Homepage loads
- [ ] Our Story page shows milestones
- [ ] Admin dashboard accessible
- [ ] Can log in
- [ ] Milestone management works
- [ ] Images display correctly

---

## 🔄 Update Workflow

For future updates:

1. **Make changes locally**
2. **Test locally**
3. **Commit and push to git**
4. **SSH to server**
5. **Run: `./deploy.sh`**
6. **Verify changes**

---

## 🆘 Quick Fixes

### Static files not loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database locked error
```bash
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3
```

### Gunicorn won't start
```bash
sudo journalctl -u gunicorn -f
# Check the error and fix
sudo systemctl restart gunicorn
```

### 502 Bad Gateway
```bash
sudo systemctl status gunicorn
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 📞 Need Help?

Check logs:
```bash
# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

---

**Server:** 178.104.213.200  
**Project Path:** /var/www/rotom  
**Domain:** rotomethiopia.org (when configured)
