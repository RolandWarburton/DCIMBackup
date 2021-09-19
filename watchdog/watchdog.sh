#!/bin/sh

# ==================================================================================================
# AUTHOR: Roland Warburton
# DATE: 19/09/2021
# EMAIL: warburtonroland@gmail.com
# ==================================================================================================
# Install inotify-tools for the inotifywait command

echo "running watchdog service"

MONITORDIR="/home/roland/mobile_photos"

inotifywait -m -r -e create --format '%w%f' "${MONITORDIR}" | while read NEWFILE
do
    curl -d "{\"data\":\"${NEWFILE}\"}" -H "Content-Type: application/json" -X POST http://desktop.rolandw.lan:8001
done

