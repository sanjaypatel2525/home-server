#!/bin/bash
# Just dump the DB to a fixed file
# No zipping, no timestamping (Duplicati handles versions)
ROOT=/home/dj5254/server1
MEDIA=/home-server-media
/snap/bin/docker exec firefly_iii_db /usr/bin/mariadb-dump -u firefly -ppassword firefly > $ROOT$MEDIA/resilio-data/folders/ResilioSync/photoprism_ignore/fireflyiii/backups/firefly_latest.sql