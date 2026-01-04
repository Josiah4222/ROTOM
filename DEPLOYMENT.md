# ROTOM Ethiopia VPS Deployment Guide

## Prerequisites
- Ubuntu 22.04.5 LTS VPS
- Root or sudo access
- Domain name (optional but recommended)

## Step 1: Prepare Your VPS

1. **Connect to your VPS:**
   ```bash
   ssh root@YOUR_VPS_IP
   ```

2. **Run the deployment script:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

## Step 2: Configure Environment Variables

1. **Update .env file:**
   ```bash
   cp .env.production .env
   nano .env
   ```
   
   Update these values:
   - `SECRET_KEY`: Generate a new secret key
   - `VPS_IP`: Your VPS IP address
   - `DOMAIN_NAME`: Your domain name
   - `DB_PASSWORD`: Set a secure database password
   - `CHAPA_SECRET_KEY`: Your actual Chapa secret key
   - Email settings if you want newsletter functionality

## Step 3: Configure Database

1. **Update PostgreSQL password:**
   ```bash
   sudo -u postgres psql
   ALTER USER rotom_user PASSWORD 'your_secure_password';
   \q
   ```

2. **Run migrations:**
   ```bash
   source venv/bin/activate
   python manage.py migrate
   python manage.py createcachetable
   python manage.py collectstatic --noinput
   ```

## Step 4: Set Up Gunicorn Service

1. **Copy service file:**
   ```bash
   sudo cp gunicorn.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

2. **Check status:**
   ```bash
   sudo systemctl status gunicorn
   ```

## Step 5: Configure Nginx

1. **Copy Nginx configuration:**
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/rotom
   sudo ln -s /etc/nginx/sites-available/rotom /etc/nginx/sites-enabled/
   ```

2. **Update the configuration:**
   ```bash
   sudo nano /etc/nginx/sites-available/rotom
   ```
   Replace `YOUR_VPS_IP` and `yourdomain.com` with your actual values.

3. **Test and restart Nginx:**
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Step 6: Create Superuser

```bash
source venv/bin/activate
python manage.py createsuperuser
```

## Step 7: Set Up SSL (Optional but Recommended)

1. **Install Certbot:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Get SSL certificate:**
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Update .env for SSL:**
   ```bash
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   SECURE_HSTS_SECONDS=31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS=True
   SECURE_HSTS_PRELOAD=True
   ```

4. **Restart services:**
   ```bash
   sudo systemctl restart gunicorn
   sudo systemctl restart nginx
   ```

## Step 8: Set Up Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Maintenance Commands

- **Restart application:** `sudo systemctl restart gunicorn`
- **View logs:** `sudo journalctl -u gunicorn -f`
- **Update static files:** `python manage.py collectstatic --noinput`
- **Database backup:** `pg_dump rotom_db > backup.sql`

## Troubleshooting

1. **Check Gunicorn logs:**
   ```bash
   sudo journalctl -u gunicorn -f
   ```

2. **Check Nginx logs:**
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

3. **Test database connection:**
   ```bash
   python manage.py dbshell
   ```

## Security Checklist

- [ ] Changed default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configured firewall
- [ ] Set up SSL certificate
- [ ] Updated database password
- [ ] Configured proper file permissions
- [ ] Set up regular backups

Your ROTOM Ethiopia website should now be live at your VPS IP address or domain name!