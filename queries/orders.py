
import csv

from models.order import Order
from models.search_result import SearchResult

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

def search_buses(query, recorded_bus_numbers):
    results = []
    for order in orders:
        order_string = str(order)
        for bus_number in order.range:
            bus_number_string = f'{bus_number:04d}'
            match = 0
            if query in bus_number_string:
                match += (len(query) / len(bus_number_string)) * 100
                if bus_number_string.startswith(query):
                    match += len(query)
            if bus_number not in recorded_bus_numbers:
                match /= 10
            results.append(SearchResult('bus', bus_number_string, order_string, f'bus/{bus_number}', match))
    return [r for r in results if r.match > 0]
