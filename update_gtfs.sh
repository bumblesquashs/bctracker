#!/bin/sh
echo 'HELLO WORLD'
while read SYSTEM; do
    echo $SYSTEM
    mv downloads/gtfs/$SYSTEM.zip archives/gtfs/$SYSTEM-$(date +%F-%T).zip
    echo 'TEST 1'
    wget -O downloads/gtfs/$SYSTEM.zip http://$SYSTEM.mapstrat.com/current/google_transit.zip
    echo 'TEST 2'
    rm -rf data/gtfs/$SYSTEM
    echo 'TEST 3'
    unzip downloads/gtfs/$SYSTEM.zip -d data/gtfs/$SYSTEM
    echo 'TEST 4'
done < systems.txt
