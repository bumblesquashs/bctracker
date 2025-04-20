#!/bin/sh

# Install Python dependencies
# In environments supporting Python 2 and 3, replace pip with pip3 before running
pip install requests
pip install Bottle
pip install cherrypy
pip install wsgi-request-logger
pip install protobuf==3.20
pip install google
pip install python-crontab
pip install pytz

# Create directories
mkdir -p archives/gtfs
mkdir -p archives/realtime

mkdir -p data/gtfs
mkdir -p data/realtime

mkdir -p logs

mkdir -p backups
