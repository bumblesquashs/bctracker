
from models.date import Date
from models.time import Time

import queries.record
import queries.transfer

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
        
        records = queries.record.find_all(bus_number=bus.number, limit=1)
        if len(records) > 0:
            last_record = records[0]
            if last_record.system != system:
                queries.transfer.create(bus, today, last_record.system, system)
            if last_record.date == today and last_record.block_id == block.id:
                queries.record.update(last_record.id, now)
                trip_ids = queries.record.find_trip_ids(last_record)
                if trip.id not in trip_ids:
                    queries.record.create_trip(last_record.id, trip)
                continue
        queries.record.create(bus, today, system, block, now, trip)
    database.commit()
