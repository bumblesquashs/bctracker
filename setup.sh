#!/bin/sh

# Install Python dependencies
# In environments supporting Python 2 and 3, replace pip with pip3 before running
pip3 install wget
pip3 install Bottle
pip3 install cherrypy
pip3 install wsgi-request-logger
pip3 install protobuf
pip3 install google
pip3 install python-crontab

# Create directories
mkdir -p archives/gtfs
mkdir -p archives/realtime

mkdir -p data/gtfs
mkdir -p data/history
mkdir -p data/realtime

mkdir -p downloads/gtfs
mkdir -p downloads/realtime

mkdir -p logs

# Load latest GTFS and realtime
chmod +x update_gtfs.sh
chmod +x update_realtime.sh
./update_gtfs.sh
./update_realtime.sh

# cp downloads/realtime
# if [ ! -f downloads/realtime/last_seen.json ]
#   then cp downloads/realtime/last_seen.json.seed downloads/realtime/last_seen.json
# fi
# mkdir -p data/realtime_downloads
# mkdir -p logs
# mkdir -p data/nextride
# mkdir -p data/nextride/archived-route-json
# mkdir -p data/vehicle_history/vehicle
