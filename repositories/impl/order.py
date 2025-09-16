
from dataclasses import dataclass, field
import json

from models.context import Context
from models.match import Match
from models.order import Order
from models.vehicle import Vehicle

import repositories

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
        repositories.livery.load()
        id = 1
        with open(f'./static/orders.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = repositories.agency.find(agency_id)
                agency_orders = {}
                agency_vehicles = {}
                for (model_id, model_values) in agency_values.items():
                    model = repositories.model.find(model_id)
                    for values in model_values:
                        order = Order.from_json(id, agency, model, values)
                        agency_orders[id] = order
                        for vehicle in order.vehicles:
                            agency_vehicles[vehicle.id] = vehicle
                        id += 1
                self.orders[agency_id] = agency_orders
                self.vehicles[agency_id] = agency_vehicles
    
    def find_vehicle(self, context: Context, id: str) -> Vehicle | None:
        try:
            return self.vehicles[context.agency_id][id]
        except:
            if context.vehicle_name_length:
                try:
                    int_id = int(id)
                    name = f'{int_id:0{context.vehicle_name_length}d}'
                except:
                    name = id[:context.vehicle_name_length]
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
    
    def find_matches(self, context: Context, query: str, recorded_vehicle_ids: set[str]) -> list[Match]:
        '''Returns matching vehicles for a given query'''
        matches = []
        try:
            vehicles = self.vehicles[context.agency_id].values()
        except KeyError:
            vehicles = [b for a in self.vehicles.values() for b in a.values()]
        for vehicle in vehicles:
            if not vehicle.visible:
                continue
            year_model = vehicle.year_model or 'Unknown year/model'
            if vehicle.model and vehicle.model.type:
                model_icon = f'model/type/{vehicle.model.type.image_name}'
                title_prefix = vehicle.model.type.title_prefix
            else:
                model_icon = 'ghost'
                title_prefix = None
            value = 0
            if query in vehicle.name:
                value += (len(query) / len(vehicle.name)) * 100
                if vehicle.name.startswith(query):
                    value += len(query)
            if vehicle.id not in recorded_vehicle_ids:
                value /= 10
            decoration = vehicle.find_decoration()
            name = vehicle.name
            if decoration and decoration.enabled:
                name += f' {decoration}'
            if title_prefix:
                name = f'{title_prefix} {name}'
            matches.append(Match(name, year_model, model_icon, f'bus/{vehicle.url_id}', value))
        return matches
