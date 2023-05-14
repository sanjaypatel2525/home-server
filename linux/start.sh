#!/bin/bash

echo "Loading crontab file: /media1/crontab"

# Load the crontab file
crontab /media1/crontab

# Start cron
echo "Starting cron..."
crond -f