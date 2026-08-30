
from dataclasses import dataclass

from database import Database

from models.context import Context
from models.departure import Departure, PickupType, DropoffType

@dataclass(slots=True)
class DepartureRepository:
    
    database: Database
    
    def create(self, download_id: int, context: Context, row: dict):
        '''Inserts a new departure into the database'''
        try:
            pickup_type = PickupType(row['pickup_type'])
        except (KeyError, ValueError):
            pickup_type = PickupType.NORMAL
        try:
            dropoff_type = DropoffType(row['drop_off_type'])
        except (KeyError, ValueError):
            dropoff_type = DropoffType.NORMAL
        try:
            timepoint = row['timepoint'] == '1'
        except KeyError:
            timepoint = False
        try:
            distance = int(row['shape_dist_traveled'])
        except (KeyError, ValueError):
            distance = None
        try:
            headsign = row['stop_headsign']
        except KeyError:
            headsign = None
        self.database.insert(
            table='departure',
            values={
                'download_id': download_id,
                'trip_id': row['trip_id'],
                'sequence': int(row['stop_sequence']),
                'stop_id': row['stop_id'],
                'time': row['departure_time'],
                'pickup_type': pickup_type.value,
                'dropoff_type': dropoff_type.value,
                'timepoint': 1 if timepoint else 0,
                'distance': distance,
                'headsign': headsign
            }
        )
    
    def find(self, context: Context, trip_id: str, sequence: int) -> Departure:
        '''Returns the departure with the given context, trip, sequence, and stop'''
        departures = self.find_all(context, trip_id, sequence)
        try:
            return departures[0]
        except IndexError:
            return None
    
    def find_all(self, context: Context, trip_id: str | None = None, sequence: int | None = None, route_id: str | None = None, stop_id: str | None = None, block_id: str | None = None, limit: int | None = None) -> list[Departure]:
        '''Returns all departures that match the given context, trip, sequence, and stop'''
        if trip_id:
            order_by = 'departure.sequence ASC'
        elif stop_id:
            order_by = [
                'departure.time ASC',
                'departure.sequence DESC'
            ]
        else:
            order_by = None
        joins = {
            'download': {
                'download.download_id': 'departure.download_id'
            }
        }
        if route_id or block_id:
            joins['trip'] = {
                'trip.download_id': 'departure.download_id',
                'trip.trip_id': 'departure.trip_id'
            }
        return self.database.select(
            table='departure',
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'departure.trip_id': 'trip_id',
                'departure.sequence': 'sequence',
                'departure.stop_id': 'stop_id',
                'departure.time': 'time',
                'departure.pickup_type': 'pickup_type',
                'departure.dropoff_type': 'dropoff_type',
                'departure.timepoint': 'timepoint',
                'departure.distance': 'distance',
                'departure.headsign': 'headsign'
            },
            joins=joins,
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
                'departure.trip_id': trip_id,
                'departure.sequence': sequence,
                'departure.stop_id': stop_id,
                'trip.block_id': block_id,
                'trip.route_id': route_id
            },
            order_by=order_by,
            limit=limit,
            initializer=Departure.from_db
        )
    
    def find_upcoming(self, context: Context, trip_id: str, sequence: int, limit: int | None = None) -> list[Departure]:
        '''Returns all departures on a trip from the given sequence number onwards'''
        return self.database.select(
            table='departure',
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'departure.trip_id': 'trip_id',
                'departure.sequence': 'sequence',
                'departure.stop_id': 'stop_id',
                'departure.time': 'time',
                'departure.pickup_type': 'pickup_type',
                'departure.dropoff_type': 'dropoff_type',
                'departure.timepoint': 'timepoint',
                'departure.distance': 'distance',
                'departure.headsign': 'headsign'
            },
            joins={
                'download': {
                    'download.download_id': 'departure.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
                'departure.trip_id': trip_id,
                'departure.sequence': {
                    '>=': sequence
                }
            },
            order_by='departure.sequence',
            limit=limit,
            initializer=Departure.from_db
        )
    
    def find_adjacent(self, context: Context, stop_id: str) -> list[Departure]:
        '''Returns all departures on trips that serve the given stop'''
        cte, args = self.database.build_select(
            table='departure',
            columns='trip.*',
            joins={
                'download': {
                    'download.download_id': 'departure.download_id'
                },
                'trip': {
                    'trip.download_id': 'departure.download_id',
                    'trip.trip_id': 'departure.trip_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
                'departure.stop_id': stop_id
            })
        return self.database.select(
            table='stop_trip',
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'departure.trip_id': 'trip_id',
                'departure.sequence': 'sequence',
                'departure.stop_id': 'stop_id',
                'departure.time': 'time',
                'departure.pickup_type': 'pickup_type',
                'departure.dropoff_type': 'dropoff_type',
                'departure.timepoint': 'timepoint',
                'departure.distance': 'distance',
                'departure.headsign': 'headsign'
            },
            ctes={
                'stop_trip': cte
            },
            joins={
                'download': {
                    'download.download_id': 'stop_trip.download_id'
                },
                'departure': {
                    'departure.download_id': 'stop_trip.download_id',
                    'departure.trip_id': 'stop_trip.trip_id'
                }
            },
            filters={
                'departure.stop_id': {
                    '!=': stop_id
                }
            },
            custom_args=args,
            initializer=Departure.from_db
        )
    
    def find_with_previous(self, context: Context, trip_id: str, sequence: int) -> tuple[Departure | None, Departure | None]:
        departures = self.database.select(
            table='departure',
            columns={
                'download.agency_id': 'agency_id',
                'download.system_id': 'system_id',
                'departure.trip_id': 'trip_id',
                'departure.sequence': 'sequence',
                'departure.stop_id': 'stop_id',
                'departure.time': 'time',
                'departure.pickup_type': 'pickup_type',
                'departure.dropoff_type': 'dropoff_type',
                'departure.timepoint': 'timepoint',
                'departure.distance': 'distance',
                'departure.headsign': 'headsign'
            },
            joins={
                'download': {
                    'download.download_id': 'departure.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id,
                'departure.trip_id': trip_id,
                'departure.sequence': {
                    '<=': sequence
                }
            },
            order_by='departure.sequence DESC',
            limit=2,
            initializer=Departure.from_db
        )
        if departures:
            if len(departures) == 2:
                return (departures[0], departures[1])
            return (departures[0], None)
        return (None, None)
    
    def delete_all(self, context: Context):
        '''Deletes all departures for the given context from the database'''
        download_ids = self.database.select(
            table='departure',
            columns={
                'departure.download_id': 'download_id'
            },
            distinct=True,
            joins={
                'download': {
                    'download.download_id': 'departure.download_id'
                }
            },
            filters={
                'download.agency_id': context.agency_id,
                'download.system_id': context.system_id
            },
            initializer=lambda r: r['download_id']
        )
        if not download_ids:
            return
        if len(download_ids) == 1:
            download_ids = download_ids[0]
        self.database.delete(
            table='departure',
            filters={
                'download_id': download_ids
            }
        )
