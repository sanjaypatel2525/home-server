#!/bin/bash
ROOT=/home/dj5254/server1
MEDIA=/home-server-media
BACKUP_LOC=$ROOT$MEDIA/resilio-data/folders/ResilioSync/photoprism_ignore/n8n/backups

rm -r $BACKUP_LOC/*
/snap/bin/docker exec -u node -it n8n n8n export:entities  --outputDir=/home/node/backups/

# 3. Unzip the file on the host to get individual JSON files
/usr/bin/unzip -o "$BACKUP_LOC/entities.zip" -d "$BACKUP_LOC/"

# 4. Cleanup the zip file to save space and keep Duplicati focused on the JSONs
rm "$BACKUP_LOC/entities.zip"