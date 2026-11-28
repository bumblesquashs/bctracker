
from dataclasses import dataclass, field
from glob import glob
import json

from models.context import Context
from models.match import Match
from models.order import Order
from models.vehicle import Vehicle

import repositories
import settings

@dataclass(slots=True)
class OrderRepository:
    
    orders: dict[str, dict[int, Order]] = field(default_factory=dict)
    vehicles: dict[str, dict[str, Vehicle]] = field(default_factory=dict)
    
    def load(self):
        '''Loads order data from the static JSON file'''
        self.orders = {}
        self.vehicles = {}
        repositories.agency.load()
        repositories.model.load()
        id = 1
        root_path = f'./config/{settings.current.province.path_id}/agencies'
        file_name = 'orders.json'
        agency_paths = glob(f'{root_path}/*/{file_name}')
        for path in agency_paths:
            with open(path, 'r') as file:
                values = json.load(file)
            agency_id = path[len(root_path):-len(file_name)].strip('/')
            agency = repositories.agency.find(agency_id)
            orders = {}
            vehicles = {}
            for order_data in values:
                order = Order.from_json(id, agency, order_data)
                orders[id] = order
                for vehicle in order.vehicles:
                    vehicles[vehicle.id] = vehicle
                id += 1
            self.orders[agency_id] = orders
            self.vehicles[agency_id] = vehicles
    
    def find_vehicle(self, context: Context, id: str) -> Vehicle | None:
        try:
            return self.vehicles[context.agency_id][id]
        except:
            vehicle_name_length = context.config.vehicle_name_length
            if vehicle_name_length:
                try:
                    int_id = int(id)
                    name = f'{int_id:0{vehicle_name_length}d}'
                except:
                    name = id[:vehicle_name_length]
            else:
                name = id
            return Vehicle(context.agency, id, name)
    
    def find_order(self, context: Context, id: int) -> Order | None:
        try:
            return self.orders[context.agency_id][id]
        except KeyError:
            return None
    
    def find_all(self, context: Context) -> list[Order]:
        '''Returns all orders'''
        if context.agency:
            try:
                return sorted(self.orders[context.agency_id].values())
            except KeyError:
                return []
        return sorted([o for a in self.orders.values() for o in a.values()])
    
    def find_vehicles(self, id: str) -> list[Vehicle]:
        '''Returns all vehicles with the given ID'''
        vehicles = []
        for agency_vehicles in self.vehicles.values():
            if id in agency_vehicles:
                vehicle = agency_vehicles[id]
                if vehicle.agency.config.enabled and vehicle.visible:
                    vehicles.append(vehicle)
        return vehicles
    
    def find_matches(self, context: Context, query: str, recorded_vehicle_ids: set[str]) -> list[Match]:
        '''Returns matching vehicles for a given query'''
        query = query.lower()
        matches = []
        try:
            vehicles = self.vehicles[context.agency_id].values()
        except KeyError:
            vehicles = [b for a in self.vehicles.values() for b in a.values()]
        for vehicle in vehicles:
            if not vehicle.agency.config.enabled or not vehicle.visible:
                continue
            value = 0
            name = vehicle.name.lower()
            if query in name:
                value += (len(query) / len(name)) * 100
                if name.startswith(query):
                    value += len(query)
            if vehicle.id not in recorded_vehicle_ids:
                value /= 10
            matches.append(Match.vehicle(vehicle, value))
        return matches
