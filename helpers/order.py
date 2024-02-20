
import json

from models.match import Match
from models.order import Order

import helpers.agency
import helpers.model

orders = {}

def load():
    '''Loads order data from the static JSON file'''
    global orders
    orders = {}
    helpers.agency.load()
    helpers.model.load()
    with open(f'./static/orders.json', 'r') as file:
        for (agency_id, agency_values) in json.load(file).items():
            agency = helpers.agency.find(agency_id)
            agency_orders = []
            for (model_id, model_values) in agency_values.items():
                model = helpers.model.find(model_id)
                for values in model_values:
                    agency_orders.append(Order(agency, model, **values))
            orders[agency_id] = agency_orders

def find(agency, bus):
    '''Returns the order containing the given bus number'''
    agency_id = getattr(agency, 'id', agency)
    bus_number = getattr(bus, 'number', bus)
    if agency_id in orders and bus_number >= 0:
        agency_orders = orders[agency_id]
        for order in agency_orders:
            if bus_number in order:
                return order
    return None

def find_all(agency=None):
    '''Returns all orders'''
    agency_id = getattr(agency, 'id', agency)
    if agency_id is None:
        return [o for a in orders.values() for o in a]
    return orders[agency_id]

def find_matches(agency, query, recorded_bus_numbers):
    '''Returns matching buses for a given query'''
    matches = []
    orders = find_all(agency)
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
