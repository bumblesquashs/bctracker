
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

def find(bus_number):
    '''Returns the order containing the given bus number'''
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
        for bus in order:
            bus_number_string = str(bus)
            value = 0
            if query in bus_number_string:
                value += (len(query) / len(bus_number_string)) * 100
                if bus_number_string.startswith(query):
                    value += len(query)
            if bus.number not in recorded_bus_numbers:
                value /= 10
            icon = bus.icon
            if icon is not None and icon.enabled:
                bus_number_string += f' {icon}'
            matches.append(Match('bus', bus_number_string, order_string, f'bus/{bus.number}', value))
    return matches

def delete_all():
    '''Deletes all orders'''
    global orders
    orders = []
