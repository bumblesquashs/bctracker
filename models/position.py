
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.system import System

from dataclasses import dataclass

from models.adherence import Adherence
from models.bus import Bus
from models.occupancy import Occupancy
from models.row import Row
from models.timestamp import Timestamp

import repositories

@dataclass(slots=True)
class Position:
    '''Current information about a bus' coordinates, trip, and stop'''
    
    system: System
    bus: Bus
    trip_id: str | None
    stop_id: str | None
    block_id: str | None
    route_id: str | None
    sequence: int | None
    lat: float | None
    lon: float | None
    bearing: float | None
    speed: float | None
    adherence: Adherence | None
    occupancy: Occupancy | None
    timestamp: Timestamp
    
    @classmethod
    def from_db(cls, row: Row):
        '''Returns a position initialized from the given database row'''
        context = row.context()
        bus = Bus.find(context, row['bus_number'])
        trip_id = row['trip_id']
        stop_id = row['stop_id']
        block_id = row['block_id']
        route_id = row['route_id']
        sequence = row['sequence']
        lat = row['lat']
        lon = row['lon']
        bearing = row['bearing']
        speed = row['speed']
        adherence_value = row['adherence']
        if adherence_value is None:
            adherence = None
        else:
            layover = row['layover'] == 1
            adherence = Adherence(adherence_value, layover)
        occupancy = Occupancy.from_db(row['occupancy'])
        timestamp = Timestamp.parse(row['timestamp'], context.timezone)
        return cls(context.system, bus, trip_id, stop_id, block_id, route_id, sequence, lat, lon, bearing, speed, adherence, occupancy, timestamp)
    
    @property
    def context(self):
        '''The context for this position'''
        return self.system.context
    
    @property
    def has_location(self):
        '''Checks if this position has non-null coordinates'''
        return self.lat is not None and self.lon is not None
    
    @property
    def trip(self):
        '''Returns the trip associated with this position'''
        if self.trip_id:
            return self.system.get_trip(self.trip_id)
        return None
    
    @property
    def stop(self):
        '''Returns the stop associated with this position'''
        if self.stop_id:
            return self.system.get_stop(stop_id=self.stop_id)
        return None
    
    @property
    def block(self):
        '''Returns the block associated with this position'''
        if not self.block_id:
            return self.system.get_block(self.block_id)
        return None
    
    @property
    def route(self):
        '''Returns the route associated with this position'''
        if not self.route_id:
            return self.system.get_route(route_id=self.route_id)
        return None
    
    @property
    def colour(self):
        '''Returns the route colour associated with this position'''
        trip = self.trip
        if trip and trip.route:
            return trip.route.colour
        return '989898'
    
    @property
    def text_colour(self):
        '''Returns the route text colour associated with this position'''
        trip = self.trip
        if trip and trip.route:
            return trip.route.text_colour
        return 'FFFFFF'
    
    @property
    def departure(self):
        '''Returns the departure associated with this position'''
        return repositories.departure.find(self.context, self.trip_id, self.sequence)
    
    def __eq__(self, other):
        return self.bus == other.bus
    
    def __lt__(self, other):
        return self.bus < other.bus
    
    def get_json(self):
        '''Returns a representation of this position in JSON-compatible format'''
        data = {
            'bus_number': self.bus.number,
            'bus_display': str(self.bus),
            'bus_url_id': str(self.bus.url_id),
            'system': str(self.system),
            'agency_id': self.context.agency_id,
            'lon': self.lon,
            'lat': self.lat,
            'colour': self.colour,
            'text_colour': self.text_colour,
            'occupancy_name': self.occupancy.value,
            'occupancy_status_class': self.occupancy.status_class,
            'occupancy_icon': self.occupancy.icon
        }
        order = self.bus.order
        if order:
            data['bus_order'] = str(order).replace("'", '&apos;')
            if order.model and order.model.type:
                data['bus_icon'] = f'model/type/bus-{order.model.type.name}'
            else:
                data['bus_icon'] = 'ghost'
        else:
            data['bus_order'] = 'Unknown Year/Model'
            data['bus_icon'] = 'ghost'
        decoration = self.bus.find_decoration()
        if decoration and decoration.enabled:
            data['decoration'] = str(decoration)
        trip = self.trip
        if trip:
            departure = self.departure
            if departure and departure.headsign:
                data['headsign'] = str(departure).replace("'", '&apos;')
            else:
                data['headsign'] = str(trip).replace("'", '&apos;')
            data['route_number'] = trip.route.number
            data['system_id'] = trip.context.system_id
            data['shape_id'] = trip.shape_id
        else:
            data['headsign'] = 'Not In Service'
            data['route_number'] = 'NIS'
        bearing = self.bearing
        if bearing is not None:
            data['bearing'] = bearing
        speed = self.speed
        if speed is not None:
            data['speed'] = speed
        adherence = self.adherence
        if adherence:
            data['adherence'] = adherence.get_json()
        timestamp = self.timestamp
        if timestamp:
            data['timestamp'] = timestamp.value
        return data
    
    def find_upcoming_departures(self):
        '''Returns the trip's upcoming departures'''
        if self.sequence is None or not self.trip:
            return []
        return repositories.departure.find_upcoming(self.context, self.trip, self.sequence)
