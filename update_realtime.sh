#!/bin/sh

while read SYSTEM; do
    mv downloads/realtime/$SYSTEM.json archives/realtime/$SYSTEM-$(date +%F-%T).json
    wget -O downloads/realtime/$SYSTEM.json https://nextride.$SYSTEM.bctransit.com/api/Route
done < systems.txt
