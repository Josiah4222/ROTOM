#!/bin/bash

# ROTOM Ethiopia Deployment Script
# This script automates the deployment process on the server

set -e  # Exit on any error

echo "=========================================="
echo "ROTOM Ethiopia Deployment Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on server
if [ ! -d "/var/www/rotom" ]; then
    echo -e "${RED}Error: This script should be run on the server in /var/www/rotom${NC}"
    exit 1
fi

cd /var/www/rotom

echo -e "${YELLOW}Step 1: Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}Step 2: Installing/updating dependencies...${NC}"
pip install -r requirements.txt

echo -e "${YELLOW}Step 3: Running database migrations...${NC}"
python manage.py migrate

echo -e "${YELLOW}Step 4: Creating cache table (if not exists)...${NC}"
python manage.py createcachetable || true

echo -e "${YELLOW}Step 5: Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${YELLOW}Step 6: Setting database permissions...${NC}"
sudo chown www-data:www-data db.sqlite3 || true
sudo chmod 664 db.sqlite3 || true
sudo chown www-data:www-data /var/www/rotom || true

echo -e "${YELLOW}Step 7: Restarting Gunicorn...${NC}"
sudo systemctl restart gunicorn

echo -e "${YELLOW}Step 8: Restarting Nginx...${NC}"
sudo systemctl restart nginx

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment completed successfully!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Visit your website to verify deployment"
echo "2. Check logs if any issues: sudo journalctl -u gunicorn -f"
echo "3. Test milestone management in admin dashboard"
echo ""
