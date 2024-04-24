
import json

from di import di

from models.match import Match
from models.order import Order

from services import AgencyService, ModelService

class DefaultOrderService:
    
    __slots__ = (
        'agency_service',
        'model_service',
        'orders'
    )
    
    def __init__(self, **kwargs):
        self.agency_service = kwargs.get('agency_service') or di[AgencyService]
        self.model_service = kwargs.get('model_service') or di[ModelService]
        self.orders = {}
    
    def load(self):
        '''Loads order data from the static JSON file'''
        self.orders = {}
        self.agency_service.load()
        self.model_service.load()
        with open(f'./static/orders.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = self.agency_service.find(agency_id)
                agency_orders = []
                for (model_id, model_values) in agency_values.items():
                    model = self.model_service.find(model_id)
                    for values in model_values:
                        agency_orders.append(Order(agency, model, **values))
                self.orders[agency_id] = agency_orders
    
    def find(self, agency, bus):
        '''Returns the order containing the given bus number'''
        agency_id = getattr(agency, 'id', agency)
        bus_number = getattr(bus, 'number', bus)
        try:
            agency_orders = self.orders[agency_id]
            for order in agency_orders:
                if bus_number in order:
                    return order
        except KeyError:
            return None
    
    def find_all(self, agency=None):
        '''Returns all orders'''
        agency_id = getattr(agency, 'id', agency)
        if agency_id:
            try:
                return self.orders[agency_id]
            except KeyError:
                return []
        return [o for a in self.orders.values() for o in a]
    
    def find_matches(self, agency, query, recorded_bus_numbers):
        '''Returns matching buses for a given query'''
        matches = []
        orders = self.find_all(agency)
        for order in orders:
            if not order.visible:
                continue
            order_string = str(order)
            if order.model is None or order.model.type is None:
                model_icon = 'ghost'
            else:
                model_icon = f'bus-{order.model.type.name}'
            for bus in order:
                bus_number_string = str(bus)
                value = 0
                if query in bus_number_string:
                    value += (len(query) / len(bus_number_string)) * 100
                    if bus_number_string.startswith(query):
                        value += len(query)
                if bus.number not in recorded_bus_numbers:
                    value /= 10
                adornment = bus.find_adornment()
                if adornment is not None and adornment.enabled:
                    bus_number_string += f' {adornment}'
                matches.append(Match(f'Bus {bus_number_string}', order_string, model_icon, f'bus/{bus.number}', value))
        return matches
