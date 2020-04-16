#!/bin/sh

DATA_DIR="$(pwd)/data"
cd $DATA_DIR
pwd
DATE_STR=$(date +%F-%T)

mv google_transit.zip archived-gtfs-static/google_transit-$DATE_STR.zip

wget http://victoria.mapstrat.com/current/google_transit.zip

rm -rf google_transit/

unzip google_transit.zip -d google_transit/
