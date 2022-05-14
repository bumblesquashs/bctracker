
import csv

from models.match import Match
from models.order import Order

orders = []

def load():
    global orders
    rows = []
    with open(f'./data/static/orders.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    orders = [Order.from_csv(row) for row in rows]

def find(bus_number):
    if bus_number < 0:
        return None
    for order in orders:
        if order.contains(bus_number):
            return order
    return None

def find_all():
    return orders

def find_matches(query, recorded_bus_numbers):
    matches = []
    for order in orders:
        order_string = str(order)
        for bus_number in order.range:
            bus_number_string = f'{bus_number:04d}'
            value = 0
            if query in bus_number_string:
                value += (len(query) / len(bus_number_string)) * 100
                if bus_number_string.startswith(query):
                    value += len(query)
            if bus_number not in recorded_bus_numbers:
                value /= 10
            matches.append(Match('bus', bus_number_string, order_string, f'bus/{bus_number}', value))
    return [m for m in matches if m.value > 0]
