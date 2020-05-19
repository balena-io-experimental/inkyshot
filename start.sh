#!/bin/bash
# Run the display update once on container start
python /usr/app/update-display.py

# Save out the current env to a file so cron job can use it
export -p > /usr/app/env.sh

# Add the job to the crontab using update_hour var, defaulting to 9 AM
(echo "0 ${UPDATE_HOUR:-9} * * * /usr/app/run-update.sh") | crontab -

# Start the cron daemon as PID 1
exec cron -f