
import wget
import time
from datetime import datetime
from datetime import date
import os.path
from os import path
import datastructure as ds
import json


#from protoc
import protobuf.data.gtfs_realtime_pb2 as rt

#use unix time
def make_realtime_filename():
    return 'gtfsrt_vehiclepos' + str(int(time.time())) + '.bin'

default_positions_file = 'data/realtime_downloads/default_gtfrealtime_VehiclePositions.bin'
vehicle_positions_path = default_positions_file
override_rt_flag = False #for debug

#global
id2fleetnum_dict = {}

victoria_gtfs_rt_url = 'http://victoria.mapstrat.com/current/gtfrealtime_VehiclePositions.bin'
last_rt_download_time = time.time()
#dynamically download the latest realtime files, save them somewhere with a logical path, update path variables here
def download_lastest_files():
    global vehicle_positions_path
    global last_rt_download_time
    print('Downloading latest gtfs-realtime files...')
    last_rt_download_time = time.time()
    fname = make_realtime_filename()
    fpath = 'data/realtime_downloads/' + fname
    try:
       wget.download(victoria_gtfs_rt_url, fpath)
       if path.exists(fpath):
           vehicle_positions_path = fpath #update path to new download
    except:
       print('victoria GTFS download failed!')
       #now, test the date to see if we are out of date
       if(int(ds.get_today_str()) > int(ds.this_sheet_enddate)):
           print('THIS SHEET IS OUT OF DATE! Please reload the server lol')
    if override_rt_flag: #for debug
        vehicle_positions_path = default_positions_file

def setup_fleetnums():
    global id2fleetnum_dict
    with open('data/nextride/id2fleetnum.json', 'r') as f:
        id2fleetnum_dict = json.load(f)

def get_data_refreshed_time_str():
    return datetime.utcfromtimestamp(last_rt_download_time).strftime('%Y-%m-%d %H:%M:%S')

class RTVehiclePosition:
  def __init__(self, fleetid, tripid, scheduled, onroute, stopid, lat, lon):
     self.fleetid = fleetid
     self.tripid = tripid
     self.scheduled = scheduled
     self.onroute = onroute
     self.stopid = stopid
     self.lat = lat
     self.lon = lon
     self.fleetnum = 'Unknown'
     self.unknown_fleetnum_flag = True


rtvehicle_dict = {}

#just for interest

busidlist = []
count_scheduled = 0
count_unsched = 0

pos_data = None
def load_realtime():
    print('Loading the realtime data now...')
    global rtvehicle_dict
    global count_scheduled
    global count_unsched
    global busidlist
    global pos_data
    count_offroute = 0
    count_scheduled = 0
    count_unsched = 0
    busidlist = []
    rtvehicle_dict = {}
    with open(vehicle_positions_path, 'rb') as vpp_f:
       feed_message = rt.FeedMessage()
       feed_message.ParseFromString(vpp_f.read())

    pos_data = feed_message.entity
    for vehicle_struct in pos_data:
       try:
          bus = vehicle_struct.vehicle
          fleetid = bus.vehicle.id
       except AttributeError:
          print('What??? No vehicle and or id in this bus?')
          continue
       try:
          trip = bus.trip
          if(bus.stop_id != ''):
              stopid = bus.stop_id
              onroute = True
          else:
              onroute = False
              stopid = 'EMPTY'
              count_offroute += 1

          tripid = trip.trip_id
          if(trip.schedule_relationship == 0 and tripid != ''):
             scheduled = True
             count_scheduled += 1
          else:
             scheduled = False
             count_unsched += 1
       except AttributeError:
          stopid = 'None: Not signed in'
          tripid = 'NONE'
          scheduled = False
          count_unsched += 1
          onroute = False
       try:
          pos = bus.position
          lat = pos.latitude
          lon = pos.longitude
       except AttributeError:
          print('No Lat Lon!')
          lat = 0
          lon = 0
       rtvehicle_dict[fleetid] = RTVehiclePosition(fleetid, tripid, scheduled, onroute, stopid, lat, lon)
       busidlist.append(fleetid)
    print('Populated the realtime structure...')
    print('Scheduled: {0} Unscheduled: {1} Total: {2}; Offroute: {3}'.format(count_scheduled, count_unsched, len(busidlist), count_offroute))
    setup_fleetnums()
    print('Fleet number translation list (from nextride) setup: {0} fleet numbers known'.format(len(id2fleetnum_dict)))
