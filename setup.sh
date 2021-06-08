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