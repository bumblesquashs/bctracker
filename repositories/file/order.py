
import json

from di import di

from models.context import Context
from models.match import Match
from models.order import Order

from repositories import AgencyRepository, ModelRepository, OrderRepository

class FileOrderRepository(OrderRepository):
    
    __slots__ = (
        'agency_repository',
        'model_repository',
        'orders'
    )
    
    def __init__(self, **kwargs):
        self.agency_repository = kwargs.get('agency_repository') or di[AgencyRepository]
        self.model_repository = kwargs.get('model_repository') or di[ModelRepository]
        self.orders = {}
    
    def load(self):
        '''Loads order data from the static JSON file'''
        self.orders = {}
        self.agency_repository.load()
        self.model_repository.load()
        with open(f'./static/orders.json', 'r') as file:
            for (agency_id, agency_values) in json.load(file).items():
                agency = self.agency_repository.find(agency_id)
                context = Context(agency=agency)
                agency_orders = []
                for (model_id, model_values) in agency_values.items():
                    model = self.model_repository.find(model_id)
                    for values in model_values:
                        if 'number' in values:
                            values['low'] = values['number']
                            values['high'] = values['number']
                            del values['number']
                        if 'exceptions' in values:
                            values['exceptions'] = set(values['exceptions'])
                        agency_orders.append(Order(context, model, **values))
                self.orders[agency_id] = agency_orders
    
    def find(self, context: Context, bus):
        '''Returns the order containing the given bus number'''
        bus_number = getattr(bus, 'number', bus)
        try:
            agency_orders = self.orders[context.agency_id]
            for order in agency_orders:
                if bus_number in order:
                    return order
        except KeyError:
            return None
    
    def find_all(self, context: Context):
        '''Returns all orders'''
        if context.agency:
            try:
                return self.orders[context.agency_id]
            except KeyError:
                return []
        return [o for a in self.orders.values() for o in a]
    
    def find_matches(self, context: Context, query, recorded_bus_numbers):
        '''Returns matching buses for a given query'''
        matches = []
        orders = self.find_all(context)
        for order in orders:
            if not order.visible:
                continue
            order_string = str(order)
            if not order.model or not order.model.type:
                model_icon = 'ghost'
            else:
                model_icon = f'model/type/bus-{order.model.type.name}'
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
                if adornment and adornment.enabled:
                    bus_number_string += f' {adornment}'
                matches.append(Match(f'Bus {bus_number_string}', order_string, model_icon, f'bus/{bus.url_id}', value))
        return matches
