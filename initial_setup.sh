#!/bin/sh

pip install wget
pip install Bottle
pip install cherrypy
pip install wsgi-request-logger
pip install protobuf
pip install google
DATA_DIR="$(pwd)/data"
cd $DATA_DIR
pwd
DATE_STR=$(date +%F-%T)

mkdir -p realtime_downloads
chmod +x download_new_gtfs.sh
chmod +x download_new_routes.sh
./download_new_gtfs.sh
./download_new_routes.sh
