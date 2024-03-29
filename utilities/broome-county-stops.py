
import json
import csv

with open('stops.json') as f:
    stops_json = json.load(f)

with open('data/gtfs/broome-county/stops.txt') as f:
    reader = csv.reader(f)
    columns = next(reader)
    stops_csv = [dict(zip(columns, row)) for row in reader]

result = {}

for row in stops_json:
    matching_stops = [s for s in stops_csv if s['stop_lat'] == str(row['lat']) and s['stop_lon'] == str(row['lon'])]
    if len(matching_stops) == 1:
        result[str(row['id'])] = matching_stops[0]['stop_id']
        continue
    matching_stops = [s for s in stops_csv if s['stop_desc'] == row['description']]
    if len(matching_stops) == 1:
        result[str(row['id'])] = matching_stops[0]['stop_id']
        continue
    result[str(row['id'])] = ''

with open('broome-county-stops.json', 'w') as f:
    json.dump(result, f)
