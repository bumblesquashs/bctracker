
import csv

from models.match import Match
from models.order import Order

orders = []

def load():
    '''Loads order data from the static CSV file'''
    global orders
    with open(f'./static/orders.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        orders = [Order.from_csv(dict(zip(columns, row))) for row in reader]

def find(bus):
    '''Returns the order containing the given bus number'''
    bus_number = getattr(bus, 'number', bus)
    if bus_number < 0:
        return None
    for order in orders:
        if order.contains(bus_number):
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

def delete_all():
    '''Deletes all orders'''
    global orders
    orders = []
