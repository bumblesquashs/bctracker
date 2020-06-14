#!/bin/sh

pip install wget
pip install Bottle
pip install cherrypy
pip install wsgi-request-logger
pip install protobuf
pip install google
pip install python-crontab
cp data/realtime_downloads
if [ ! -f data/realtime_downloads/last_seen.json ]
 then cp data/realtime_downloads/last_seen.json.seed data/realtime_downloads/last_seen.json
fi
mkdir -p data/realtime_downloads
mkdir -p logs
mkdir -p data/nextride
mkdir -p data/nextride/archived-route-json
mkdir -p data/vehicle_history/vehicle
chmod +x download_new_gtfs.sh
chmod +x download_new_routes.sh
./download_new_gtfs.sh
./download_new_routes.sh
