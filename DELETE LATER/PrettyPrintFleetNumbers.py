import json
f = open('data/nextride/id2fleetnum.json', 'r')
data = json.load(f)
print('List of fleet numbers: ({0} Total)'.format(len(data)))
print('Fleet Number       InternalID')
keys = list(data.keys())
for key in keys:
    print(' {0}     {1}'.format(data[str(key)], key))
vals = [int(x) for x in data.values()]
vals.sort()
for val in vals:
    print(str(val))
