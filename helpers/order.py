
import json

from models.match import Match
from models.order import Order

import helpers.model

orders = []

def load():
    '''Loads order data from the static JSON file'''
    global orders
    orders = []
    helpers.model.load()
    with open(f'./static/orders.json', 'r') as file:
        for (model_id, model_values) in json.load(file).items():
            model = helpers.model.find(model_id)
            for values in model_values:
                orders.append(Order(model=model, **values))

def find(bus):
    '''Returns the order containing the given bus number'''
    bus_number = getattr(bus, 'number', bus)
    if bus_number < 0:
        return None
    for order in orders:
        if bus_number in order:
            return order
    return None

def find_all():
    '''Returns all orders'''
    return orders

def find_matches(query, recorded_bus_numbers):
    '''Returns matching buses for a given query'''
    matches = []
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
            adornment = bus.adornment
            if adornment is not None and adornment.enabled:
                bus_number_string += f' {adornment}'
            matches.append(Match('bus', bus_number_string, order_string, model_icon, f'bus/{bus.number}', value))
    return matches
