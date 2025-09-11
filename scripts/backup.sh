#!/bin/bash

# Database Backup Script
set -e

echo "📦 Starting database backup..."

# Configuration
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="portfolio_db"
CONTAINER_NAME="portfolio_mongo_1"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create database dump
echo "🗃️  Creating database dump..."
docker exec "$CONTAINER_NAME" mongodump --db "$DB_NAME" --out "/tmp/backup_$TIMESTAMP"

# Copy backup from container
echo "📋 Copying backup from container..."
docker cp "$CONTAINER_NAME:/tmp/backup_$TIMESTAMP" "$BACKUP_DIR/"

# Compress backup
echo "🗜️  Compressing backup..."
cd "$BACKUP_DIR"
tar -czf "portfolio_backup_$TIMESTAMP.tar.gz" "backup_$TIMESTAMP"
rm -rf "backup_$TIMESTAMP"

# Cleanup old backups (keep last 7 days)
echo "🧹 Cleaning up old backups..."
find "$BACKUP_DIR" -name "portfolio_backup_*.tar.gz" -mtime +7 -delete

# Upload to cloud storage (optional)
# aws s3 cp "portfolio_backup_$TIMESTAMP.tar.gz" s3://your-backup-bucket/

echo "✅ Backup completed: portfolio_backup_$TIMESTAMP.tar.gz"
echo "📁 Backup location: $BACKUP_DIR/portfolio_backup_$TIMESTAMP.tar.gz"

# Log backup completion
echo "$(date): Backup completed - portfolio_backup_$TIMESTAMP.tar.gz" >> "$BACKUP_DIR/backup.log"