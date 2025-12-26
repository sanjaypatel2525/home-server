#!/bin/bash
# 1. Navigate to your paperless folder
ROOT=/home/dj5254/server1
DOCKER_HOME=$ROOT/home-server/paperless-ngx
cd $DOCKER_HOME

# 2. Run the exporter (Incremental mode)
docker-compose exec -T paperlesswebserver document_exporter ../export

# 3. Optional: Sync the export folder to an external drive or USB
# rsync -av --delete ./export /mnt/external_usb/paperless_backups/

echo "Backup completed on $(date)"
