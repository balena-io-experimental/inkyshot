#!/bin/bash

# Get the current device name
export DEVICE_NAME=$(curl -sX GET "https://api.balena-cloud.com/v5/device?\$filter=uuid%20eq%20'$BALENA_DEVICE_UUID'" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $BALENA_API_KEY" | \
jq -r ".d | .[0] | .device_name")

# Run the display update once on container start
python /usr/app/update-display.py

# Save out the current env to a file so cron job can use it
export -p > /usr/app/env.sh

# Set default values if these env vars are not set
if [[ -z "${ALTERNATE_FREQUENCY}" ]]; then
  Alternate="0"
  [[ -z "${UPDATE_HOUR}" ]] && UpdateHour='9' || UpdateHour="${UPDATE_HOUR}"
else
  Alternate="*/${ALTERNATE_FREQUENCY}"
  UpdateHour='*'
fi

# Add the job to the crontab using update_hour var, defaulting to 9 AM
(echo "${Alternate} ${UpdateHour} * * * /usr/app/run-update.sh > /proc/1/fd/1 2>&1") | crontab -

# Start cron 
#cron

# Start QR server
python /usr/app/server.py
