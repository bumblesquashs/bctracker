
from models.date import Date
from models.time import Time

import queries.records
import queries.transfers

import database

def update(positions):
    for position in positions:
        system = position.system
        bus = position.bus
        trip = position.trip
        if bus.number < 0 or trip is None:
            continue
        block = trip.block
        today = Date.today()
        now = Time.now()
        
        records = queries.records.find_all(bus_number=bus.number, limit=1)
        if len(records) > 0:
            last_record = records[0]
            if last_record.system != system:
                queries.transfers.create(bus, today, last_record.system, system)
            if last_record.date == today and last_record.block_id == block.id:
                queries.records.update(last_record.id, now)
                trip_ids = queries.records.find_trip_ids(last_record)
                if trip.id not in trip_ids:
                    queries.records.create_trip(last_record.id, trip)
                continue
        queries.records.create(bus, today, system, block, now, trip)
    database.commit()
