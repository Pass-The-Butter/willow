#!/bin/bash
# Housekeeping: Backup Population Database
# Usage: ./backup_population.sh [label]

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LABEL=${1:-manual}
BACKUP_DIR="$HOME/backups/population"
FILENAME="population_${TIMESTAMP}_${LABEL}.sql.gz"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

echo "🧹 Housekeeping: Starting Backup of Population DB..."
echo "   Target: $BACKUP_DIR/$FILENAME"

# Dump from Docker Container (willow-population-db)
# Note: Adjust container name if using bare metal in future
CONTAINER_NAME="willow-population-db"

if docker ps | grep -q $CONTAINER_NAME; then
    docker exec -t $CONTAINER_NAME pg_dump -U willow -d population | gzip > "$BACKUP_DIR/$FILENAME"
    
    # Verify file size
    SIZE=$(du -h "$BACKUP_DIR/$FILENAME" | cut -f1)
    echo "✅ Backup Complete. Size: $SIZE"
    
    # Retention Policy: Keep last 10
    echo "   Cleaning up old backups (keeping last 10)..."
    ls -tp "$BACKUP_DIR"/population_*.sql.gz | grep -v '/$' | tail -n +11 | xargs -I {} rm -- {}
else
    echo "❌ Error: Container '$CONTAINER_NAME' not running. Skipping backup."
    exit 1
fi
