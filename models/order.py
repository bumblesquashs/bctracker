
import csv

from models.model import get_model

class Order:
    def __init__(self, low, high, year, model_id):
        self.low = low
        self.high = high
        self.year = year
        self.model_id = model_id
        
        self.size = (high - low) + 1
    
    def __str__(self):
        model = self.model
        if model is None:
            return str(self.year)
        return f'{self.year} {model}'
    
    def __eq__(self, other):
        return self.low == other.low and self.high == other.high
    
    @property
    def model(self):
        return get_model(self.model_id)
    
    def contains(self, bus):
        return self.low <= bus.number <= self.high

orders = []

def load_orders():
    rows = []
    with open(f'./static_data/orders.csv', 'r') as file:
        reader = csv.reader(file)
        columns = next(reader)
        for row in reader:
            rows.append(dict(zip(columns, row)))
    for row in rows:
        low = int(row['low'])
        high = int(row['high'])
        year = int(row['year'])
        model_id = row['model_id']

        orders.append(Order(low, high, year, model_id))

def get_order(bus):
    for order in orders:
        if order.contains(bus):
            return order
    return None
