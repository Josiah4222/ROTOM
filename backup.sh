#!/bin/bash

# Backup script for ROTOM Ethiopia (SQLite version)
# Add to crontab: 0 2 * * * /var/www/rotom/backup.sh

BACKUP_DIR="/var/backups/rotom"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/var/www/rotom"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup SQLite database
echo "Backing up SQLite database..."
cp $PROJECT_DIR/db.sqlite3 $BACKUP_DIR/db_backup_$DATE.sqlite3

# Backup media files
echo "Backing up media files..."
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz $PROJECT_DIR/media/

# Backup .env file
echo "Backing up environment file..."
cp $PROJECT_DIR/.env $BACKUP_DIR/env_backup_$DATE

# Remove backups older than 30 days
echo "Cleaning old backups..."
find $BACKUP_DIR -name "*.sqlite3" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "env_backup_*" -mtime +30 -delete

echo "Backup completed: $DATE"
echo "Database backup: $BACKUP_DIR/db_backup_$DATE.sqlite3"
