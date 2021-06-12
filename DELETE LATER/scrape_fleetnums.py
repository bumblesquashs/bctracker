import json
import urllib.request


added_list = []

# maintains the id2fleetnum json file
def updateTable(api_json_data):
    global added_list
    # read in existing table if any
    try:
        f = open('data/nextride/id2fleetnum.json', 'r')
        id2fleetnum_dict = json.load(f)
        f.close()
    except:
        print("Couldn't load json, so creating new file")
        id2fleetnum_dict = {}
        f.close()
    print('Number of fleet numbers in table: ' +
          str(len(id2fleetnum_dict.keys())))

    # update table with the api data given
    added = 0
    for obj in api_json_data:
        try:
            # json writes out to strings, so always use strings even though the api data has ints
            fleet_num = str(obj['name'])
            fleet_id = str(obj['vehicleId'])
            if(fleet_id not in id2fleetnum_dict):
                id2fleetnum_dict[fleet_id] = fleet_num
                added += 1
                added_list.append(fleet_num)
        except KeyError:
            print('Error: fleet number or vehicleID missing')
        except ValueError:
            print("Couldn't convert fleetID to int: weird fleetid in file?")
    print('Added {0} entries; new count: {1} '.format(
        added, str(len(id2fleetnum_dict.keys()))))

    # write table back out
    with open('data/nextride/id2fleetnum.json', 'w') as out_f:
        json.dump(id2fleetnum_dict, out_f)


def scrape():
    # this file should be:
    # https://nextride.victoria.bctransit.com/api/Route
    with open('data/nextride/Route.json', 'r') as f:
        active_routes_data = json.load(f)

    pattern_numbers = []
    for obj in active_routes_data:
        pattern_numbers.append(obj['patternID'])

    url_base = 'https://nextride.victoria.bctransit.com/api/VehicleStatuses?patternIds='
    dumbo = '' # dumbo the giant query string
    for pattern_num in pattern_numbers:
        dumbo += str(pattern_num) + ','
    dumbo = dumbo[:-1]  # drop trailing comma
    the_god_query = url_base + dumbo
    print('The query has been obtained and saved from nextride. Here we go.')
    with open('data/nextride/godquery.txt', 'w') as f:
        f.write(the_god_query)

    # use the god query
    with urllib.request.urlopen(the_god_query) as response:
        result = response.read()
        json_data = json.loads(result)
    print("We've apparently read {0} busses from nextride".format(
        len(json_data)))
    print('Successfully queried NextRide... adding to table')
    updateTable(json_data)

    with open('data/nextride/last_api_result.json', 'w') as f:
        f.write(str(result))
