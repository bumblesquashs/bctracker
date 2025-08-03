
from dataclasses import dataclass, field
import json

from models.bus import Bus
from models.context import Context
from models.match import Match
from models.order import Order

import repositories

@dataclass(slots=True)
class OrderRepository:
    
    orders: dict[str, dict[int, Order]] = field(default_factory=dict)
    buses: dict[str, dict[str, Bus]] = field(default_factory=dict)
    
    def load(self):
        '''Loads order data from the static JSON file'''
        self.orders = {}
        self.buses = {}
        repositories.agency.load()
        repositories.model.load()
        repositories.livery.load()
        id = 1
        with open(f'./static/orders.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = repositories.agency.find(agency_id)
                agency_orders = {}
                agency_buses = {}
                for (model_id, model_values) in agency_values.items():
                    model = repositories.model.find(model_id)
                    for values in model_values:
                        order = Order.from_json(id, agency, model, values)
                        agency_orders[id] = order
                        for bus in order.buses:
                            agency_buses[bus.id] = bus
                        id += 1
                self.orders[agency_id] = agency_orders
                self.buses[agency_id] = agency_buses
    
    def find_bus(self, context: Context, number: str) -> Bus | None:
        try:
            return self.buses[context.agency_id][number]
        except:
            if context.vehicle_name_length:
                try:
                    int_number = int(number)
                    name = f'{int_number:0{context.vehicle_name_length}d}'
                except:
                    name = number[:context.vehicle_name_length]
            else:
                name = number
            return Bus(context.agency, number, name)
    
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
    
    def find_matches(self, context: Context, query, recorded_vehicle_ids) -> list[Match]:
        '''Returns matching buses for a given query'''
        matches = []
        try:
            buses = self.buses[context.agency_id].values()
        except KeyError:
            buses = [b for a in self.buses.values() for b in a.values()]
        for bus in buses:
            if not bus.visible:
                continue
            year_model = bus.year_model or 'Unknown year/model'
            if not bus.model or not bus.model.type:
                model_icon = 'ghost'
            else:
                model_icon = f'model/type/bus-{bus.model.type.name}'
            value = 0
            if query in bus.name:
                value += (len(query) / len(bus.name)) * 100
                if bus.name.startswith(query):
                    value += len(query)
            if bus.id not in recorded_vehicle_ids:
                value /= 10
            decoration = bus.find_decoration()
            name = bus.name
            if decoration and decoration.enabled:
                name += f' {decoration}'
            matches.append(Match(f'Bus {name}', year_model, model_icon, f'bus/{bus.url_id}', value))
        return matches
