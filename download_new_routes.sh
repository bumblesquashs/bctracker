#!/bin/sh

DATA_DIR="$(pwd)/data/nextride"
cd $DATA_DIR
pwd
DATE_STR=$(date +%F-%T)

mv Route.json archived-route-json/Route-$DATE_STR.json

wget -O Route.json https://nextride.victoria.bctransit.com/api/Route
