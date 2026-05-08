# Pre-Deployment Checklist for ROTOM Ethiopia

## ✅ Completed Tasks

### 1. Database & Migrations
- [x] All models created (Milestone, TeamMember, etc.)
- [x] Migrations generated
- [x] Migrations applied locally
- [x] Initial data added (7 milestones)

### 2. Static Files
- [x] Static files collected
- [x] CSS files in place
- [x] Images organized
- [x] WhiteNoise configured for production

### 3. Templates
- [x] All templates created
- [x] Dynamic milestone loading implemented
- [x] Admin dashboard templates ready

### 4. Admin Dashboard
- [x] Milestone management views created
- [x] Forms configured
- [x] URLs mapped
- [x] Sidebar navigation updated

---

## 🔧 Pre-Deployment Tasks

### Step 1: Update Production Environment File

Create `.env.production` file with production values:

```env
SECRET_KEY=<GENERATE_NEW_SECRET_KEY>
DEBUG=False
ALLOWED_HOSTS=178.104.213.200,rotomethiopia.org,www.rotomethiopia.org

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=rotomethiopia@reachone-touchone.org
EMAIL_HOST_PASSWORD=<YOUR_APP_PASSWORD>
DEFAULT_FROM_EMAIL=ROTOM Ethiopia <rotomethiopia@reachone-touchone.org>

# Payment
CHAPA_SECRET_KEY=CHASECK-O6jk9SKQlZJcn8d9qib00WLbvzcRJreo
PAYPAL_RECEIVER_EMAIL=<YOUR_PAYPAL_EMAIL>
PAYPAL_TEST=False
```

**Generate a new SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Test Locally with Production Settings

```bash
# Set DEBUG=False in .env temporarily
DEBUG=False

# Collect static files
python manage.py collectstatic --noinput

# Run checks
python manage.py check --deploy

# Test the server
python manage.py runserver

# Verify:
# - All pages load correctly
# - Static files serve properly
# - Images display
# - Admin dashboard works
# - Milestone management works

# Set DEBUG=True back after testing
DEBUG=True
```

### Step 3: Prepare Files for Upload

```bash
# Create a deployment package (exclude unnecessary files)
# Files to EXCLUDE from upload:
# - .git/
# - __pycache__/
# - *.pyc
# - .env (use .env.production on server)
# - venv/
# - staticfiles/ (will be regenerated on server)
# - *.log
# - db.sqlite3 (will be created fresh on server)
```

### Step 4: Database Preparation

**Option A: Fresh Database (Recommended for first deployment)**
- Don't upload db.sqlite3
- Run migrations on server
- Create superuser on server
- Add milestones using the script

**Option B: Upload Existing Database**
- Upload db.sqlite3 with your data
- Ensure proper permissions on server

---

## 📦 Deployment Steps

### 1. Upload Files to Server

```bash
# From your local machine
scp -r /path/to/ROTOM/* root@178.104.213.200:/var/www/rotom/

# Or use git (recommended)
cd /var/www/rotom
git pull origin main
```

### 2. Setup on Server

```bash
# SSH into server
ssh root@178.104.213.200

# Navigate to project
cd /var/www/rotom

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Copy production environment file
cp .env.production .env

# Run migrations
python manage.py migrate

# Create cache table
python manage.py createcachetable

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Add milestones to database
python add_milestones.py

# Set permissions for SQLite
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3
sudo chown www-data:www-data /var/www/rotom

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### 3. Verify Deployment

Visit your website and check:
- [ ] Homepage loads
- [ ] All navigation links work
- [ ] Our Story page shows milestones
- [ ] Images display correctly
- [ ] Admin dashboard accessible
- [ ] Can log in to admin
- [ ] Milestone management works
- [ ] Can add/edit/delete milestones
- [ ] Forms submit correctly
- [ ] Email functionality works (if configured)

---

## 🔒 Security Checklist

- [ ] DEBUG=False in production
- [ ] New SECRET_KEY generated
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Database file permissions set (664)
- [ ] Media folder permissions set
- [ ] Firewall configured (UFW)
- [ ] SSL certificate installed (optional but recommended)
- [ ] Regular backups scheduled

---

## 🚨 Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database Permission Errors
```bash
sudo chown www-data:www-data db.sqlite3
sudo chmod 664 db.sqlite3
sudo chown www-data:www-data /var/www/rotom
```

### Gunicorn Not Starting
```bash
sudo journalctl -u gunicorn -f
# Check for errors in the log
```

### 502 Bad Gateway
```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Check Nginx error log
sudo tail -f /var/log/nginx/error.log
```

---

## 📝 Post-Deployment Tasks

1. **Test All Features**
   - Create a test milestone
   - Edit an existing milestone
   - Delete a test milestone
   - Upload images
   - Test forms

2. **Setup Monitoring**
   - Monitor server logs
   - Check error logs daily
   - Monitor disk space (SQLite database grows)

3. **Setup Backups**
   ```bash
   # Make backup.sh executable
   chmod +x backup.sh
   
   # Add to crontab for daily backups at 2 AM
   sudo crontab -e
   # Add: 0 2 * * * /var/www/rotom/backup.sh
   ```

4. **Document Admin Credentials**
   - Store superuser credentials securely
   - Share with authorized team members only

---

## 📞 Support

If you encounter issues:
1. Check logs: `sudo journalctl -u gunicorn -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify file permissions
4. Ensure all services are running

---

## ✨ New Features Deployed

### Milestone Management System
- Dynamic milestone loading from database
- Full CRUD operations via admin dashboard
- Image upload support
- Order management
- Active/Inactive status toggle
- Clean admin interface

**Access:** Dashboard → Milestones (🏁 icon in sidebar)

---

**Deployment Date:** _____________
**Deployed By:** _____________
**Server IP:** 178.104.213.200
**Domain:** rotomethiopia.org (when configured)
