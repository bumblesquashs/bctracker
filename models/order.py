
import csv

from models.model import get_model
from models.search_result import SearchResult

class Order:
    def __init__(self, row):
        self.low = int(row['low'])
        self.high = int(row['high'])
        self.year = int(row['year'])
        self.model_id = row['model_id']
        
        self.size = (self.high - self.low) + 1
    
    def __str__(self):
        model = self.model
        if model is None:
            return str(self.year)
        return f'{self.year} {model}'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        return self.low == other.low and self.high == other.high
    
    def __lt__(self, other):
        return str(self) < str(other)
    
    @property
    def model(self):
        return get_model(self.model_id)
    
    @property
    def range(self):
        return range(self.low, self.high + 1)
    
    def contains(self, bus):
        return self.low <= bus.number <= self.high

orders = []

def load_orders():
    global orders
    rows = []
    with open(f'./static_data/orders.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    orders = [Order(row) for row in rows]

def get_order(bus):
    if bus.is_unknown:
        return None
    for order in orders:
        if order.contains(bus):
            return order
    return None

def search_buses(query, recorded_buses):
    recorded_bus_numbers = [b.number for b in recorded_buses]
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
            results.append(SearchResult('bus', str(bus_number), order_string, f'bus/{bus_number}', match))
    return [r for r in results if r.match > 0]
