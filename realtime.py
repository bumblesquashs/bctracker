
from os import path, rename, remove
from datetime import datetime

import requests
import json

import protobuf.data.gtfs_realtime_pb2 as protobuf

import helpers.assignment
import helpers.departure
import helpers.overview
import helpers.position
import helpers.record
import helpers.system
import helpers.transfer

from models.adherence import Adherence
from models.date import Date
from models.time import Time

import config
import database

last_updated_date = None
last_updated_time = None

def update(system):
    '''Downloads realtime data for the given system and stores it in the database'''
    global last_updated_date, last_updated_time
    if not system.realtime_enabled:
        return
    data_path = f'data/realtime/{system.id}.bin'
    
    print(f'Updating realtime data for {system}')
    
    try:
        if system.id == 'broome-county':
            position_data = {}
            date = Date.today(system.timezone)
            time = Time.now(system.timezone)
            with open('broome-county-routes.json') as f:
                routes_json = json.load(f)
            with open('broome-county-stops.json') as f:
                stops_json = json.load(f)
            with requests.get(system.realtime_url, timeout=10) as r:
                data = json.loads(r.content)
                for bus_data in data:
                    try:
                        bus_number = int(bus_data["name"])
                        lat = bus_data["lat"]
                        lon = bus_data["lon"]
                        raw_route_id = str(bus_data["route"])
                        raw_last_stop_id = str(bus_data["lastStop"])
                        try:
                            route_id = routes_json[raw_route_id]
                        except:
                            route_id = None
                        try:
                            last_stop_id = stops_json[raw_last_stop_id]
                        except:
                            last_stop_id = None
                        if last_stop_id:
                            departures = helpers.departure.find_all(system, route=route_id, stop=last_stop_id)
                            departures = [d for d in departures if d.trip and date in d.trip.service]
                            departures.sort(key=lambda d: abs(time.get_minutes() - d.time.get_minutes()))
                            if departures:
                                departure = departures[0]
                                trip_id = departure.trip_id
                                sequence = departure.sequence
                                adherence = Adherence.calculated(departure, lat, lon)
                                if adherence:
                                    adherence = adherence.value
                            else:
                                trip_id = None
                                sequence = None
                                adherence = None
                        else:
                            trip_id = None
                            sequence = None
                            adherence = None
                        position_data[str(bus_number)] = {
                            'system_id': system.id,
                            'bus_number': bus_number,
                            'trip_id': trip_id,
                            'stop_id': last_stop_id,
                            'block_id': None,
                            'route_id': route_id,
                            'sequence': sequence,
                            'lat': lat,
                            'lon': lon,
                            'bearing': None,
                            'speed': None,
                            'adherence': adherence
                        }
                    except:
                        pass
            with open(f'data/realtime/{system.id}-positions.json', 'w') as f:
                json.dump(position_data, f)
            last_updated_date = Date.today()
            last_updated_time = Time.now(accurate_seconds=False)
            system.last_updated_date = Date.today(system.timezone)
            system.last_updated_time = Time.now(system.timezone, system.agency.accurate_seconds)
        else:
            if path.exists(data_path):
                if config.enable_realtime_backups:
                    formatted_date = datetime.now().strftime('%Y-%m-%d-%H:%M')
                    archives_path = f'archives/realtime/{system.id}_{formatted_date}.bin'
                    rename(data_path, archives_path)
                else:
                    remove(data_path)
            data = protobuf.FeedMessage()
            with requests.get(system.realtime_url, timeout=10) as r:
                if config.enable_realtime_backups:
                    with open(data_path, 'wb') as f:
                        f.write(r.content)
                data.ParseFromString(r.content)
            helpers.position.delete_all(system)
            for index, entity in enumerate(data.entity):
                vehicle = entity.vehicle
                try:
                    vehicle_id = vehicle.vehicle.id
                    vehicle_name_length = system.agency.vehicle_name_length
                    if vehicle_name_length is not None and len(vehicle_id) > vehicle_name_length:
                        vehicle_id = vehicle_id[-vehicle_name_length:]
                    bus_number = int(vehicle_id)
                except:
                    bus_number = -(index + 1)
                helpers.position.create(system, bus_number, vehicle)
            last_updated_date = Date.today()
            last_updated_time = Time.now(accurate_seconds=False)
            system.last_updated_date = Date.today(system.timezone)
            system.last_updated_time = Time.now(system.timezone, system.agency.accurate_seconds)
    except Exception as e:
        print(f'Failed to update realtime for {system}: {e}')

def update_records():
    '''Updates records in the database based on the current positions in the database'''
    try:
        for position in helpers.position.find_all():
            try:
                system = position.system
                bus = position.bus
                if bus.number < 0:
                    continue
                date = Date.today(system.timezone)
                time = Time.now(system.timezone)
                overview = helpers.overview.find(bus.number)
                trip = position.trip
                if trip is None:
                    record_id = None
                else:
                    block = trip.block
                    assignment = helpers.assignment.find(system, block)
                    if not assignment or assignment.bus_number != bus.number:
                        helpers.assignment.delete_all(system=system, block=block)
                        helpers.assignment.delete_all(bus=bus)
                        helpers.assignment.create(system, block, bus, date)
                    if overview is not None and overview.last_record is not None:
                        last_record = overview.last_record
                        if last_record.date == date and last_record.block_id == block.id:
                            helpers.record.update(last_record, time)
                            trip_ids = helpers.record.find_trip_ids(last_record)
                            if trip.id not in trip_ids:
                                helpers.record.create_trip(last_record, trip)
                            continue
                    record_id = helpers.record.create(bus, date, system, block, time, trip)
                if overview is None:
                    helpers.overview.create(bus, date, system, record_id)
                else:
                    helpers.overview.update(overview, date, system, record_id)
                    if overview.last_seen_system != system:
                        helpers.transfer.create(bus, date, overview.last_seen_system, system)
            except Exception as e:
                print(f'Failed to update records: {e}')
        database.commit()
        update_broome_county_records()
    except Exception as e:
        print(f'Failed to update records: {e}')

def update_broome_county_records():
    system = helpers.system.find('broome-county')
    date = Date.today(system.timezone)
    time = Time.now(system.timezone)
    try:
        with open(f'data/realtime/{system.id}-history.json') as f:
            history = json.load(f)
    except:
        history = {}
    positions = helpers.position.find_all(system)
    for position in positions:
        bus = position.bus
        try:
            bus_history = history[str(bus.number)]
        except:
            bus_history = {
                'system_id': system.id,
                'first_seen': date.format_db(),
                'records': []
            }
        bus_history['last_seen'] = date.format_db()
        trip = position.trip
        if trip:
            records = bus_history['records']
            trip_records = [(i, r) for (i, r) in enumerate(records) if r['trip_id'] == trip.id and r['date'] == date.format_db()]
            if trip_records:
                (index, record) = trip_records[0]
                record['last_seen'] = time.format_db()
                records[index] = record
            else:
                record = {
                    'trip_id': trip.id,
                    'date': date.format_db(),
                    'route': trip.route.number,
                    'start_time': trip.start_time.format_db(),
                    'end_time': trip.end_time.format_db(),
                    'first_seen': time.format_db(),
                    'last_seen': time.format_db()
                }
                records.append(record)
        history[str(bus.number)] = bus_history
    with open(f'data/realtime/{system.id}-history.json', 'w') as f:
        json.dump(history, f)

def get_last_updated(time_format):
    '''Returns the date/time that realtime data was last updated'''
    date = last_updated_date
    time = last_updated_time
    if date is None or time is None:
        return 'N/A'
    if date.is_today:
        return f'at {time.format_web(time_format)} {time.timezone_name}'
    return date.format_since()

def validate(system):
    '''Checks that the realtime data for the given system aligns with the current GTFS for that system'''
    if not system.realtime_enabled:
        return True
    for position in helpers.position.find_all(system):
        trip_id = position.trip_id
        if trip_id is None:
            continue
        if position.trip is None:
            trip_id_sections = trip_id.split(':')
            if len(trip_id_sections) == 3:
                block_id = trip_id_sections[2]
                if system.get_block(block_id) is None:
                    return False
            else:
                return False
    return True
