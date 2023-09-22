
import csv

import helpers.bcf_utils
from models.match import Match
from models.vehicle import Vehicle
from models.order import Order

orders = []
bcf_orders = []

def load():
    '''Loads order data from the static CSV file'''
    global orders
    global bcf_orders
    with open(f'./data/static/orders.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        orders = [Order.from_csv(dict(zip(columns, row))) for row in reader]
        bcf_orders = helpers.bcf_utils.all_bcf_orders()
        
    helpers.bcf_utils.load()

def find(id, is_named):
    '''Returns the order containing the given vehicle id'''
    if is_named:
        # Must be a ferry, right now
        return bcf_utils.get_order(id)
    bus_number = int(id)
    if bus_number < 0:
        return None
    for order in orders:
        if order.contains(bus_number):
            return order
    return None

def find_all():
    '''Returns all orders'''
    return orders
    
def find_all_bcf_orders():
    '''Returns all bcf_orders'''
    return bcf_orders

def find_matches(query, recorded_bus_numbers):
    '''Returns matching buses for a given query'''
    matches = []
    for order in orders:
        if order.is_test:
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
            adornment = bus.adornment
            if adornment is not None and adornment.enabled:
                bus_number_string += f' {adornment}'
            matches.append(Match('bus', bus_number_string, order_string, f'bus/{bus.number}', value))
    return matches

def delete_all():
    '''Deletes all orders'''
    global orders
    global bcf_orders
    orders = []
    bcf_orders = []
