import re
import requests
from datetime import datetime

from bs4 import BeautifulSoup


bcf_routes = [
    {
        "name": "Vancouver - Victoria (Tsawwassen-Swartz Bay)",
        "major": True,
        "route_number": 1,
        "vessel_tracking": {
            "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route0.jpg",
            "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route0.html",
            "top": 49.090570, 
            "right": -122.957330,
            "bottom": 48.640203, 
            "left": -123.638279
        }
    },
    {
        "name": "West Vancouver - Nanaimo (Horseshoe Bay-Departure Bay)",
        "major": True,
        "route_number": 2,
        "vessel_tracking": {
            "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route3.jpg",
            "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route3.html",
            "top": 49.670018, 
            "right": -122.910209,
            "bottom": 48.782737, 
            "left": -124.271125
        }
    },
    {
        "name": "West Van - Sunshine Coast (Horseshoe Bay-Langdale)",
        "major": True,
        "route_number": 3,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route4.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route4.html",
          "top": 49.508268, 
          "right": -123.218880,
          "bottom": 49.290202, 
          "left": -123.565292
        }
    },
    {
        "name": "Salt Spring Island - Victoria (Fulford Harbour - Swartz Bay)",
        "major": False,
        "route_number": 4,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route6.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route6.html",
          "top": 48.874651, 
          "right": -123.259735,
          "bottom": 48.655139, 
          "left": -123.605804
        }
    },
    {
        "name": "Southern Gulf Islands",
        "major": False,
        "route_number": 5,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route7.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route7.html",
          "top": 49.029089, 
          "right": -123.014774,
          "bottom": 48.584557, 
          "left": -123.693352
        }
    },
    {
        "name": "Salt Spring Island (Vesuvius Bay - Crofton)",
        "major": False,
        "route_number": 6,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route17.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route17.html"
        }
    },
    {
        "name": "Sechelt - Powell River (Earls Cove-Saltery Bay)",
        "major": False,
        "route_number": 7,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route29.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route29.html",
          "top": 49.882469, 
          "right": -123.912735,
          "bottom": 49.664517, 
          "left": -124.255714
        }
    },
    {
        "name": "Bowen Island - Vancouver (Snug Cove-Horseshoe Bay)",
        "major": False,
        "route_number": 8,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route5.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route5.html",
          "top": 49.435427, 
          "right": -123.228149,
          "bottom": 49.325570, 
          "left": -123.396721
        }
    },
    {
        "name": "Southern Gulf Islands",
        "major": False,
        "route_number": 9,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route2.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route2.html"
        }
    },
    {
        "name": "Inside Passage",
        "major": False,
        "route_number": 10,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.html"
        }
    },
    {
        "name": "Haida Gwaii (Prince Rupert - Skidegate)",
        "major": False,
        "route_number": 11,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.html"
        }
    },
    {
        "name": "Brentwood Bay - Mill Bay (Saanich Peninsula - Vancouver Island)",
        "major": False,
        "route_number": 12,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route16.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route16.html",
          "top": 48.648562, 
          "right": -123.407192,
          "bottom": 48.536841, 
          "left": -123.582115
        }
    },
    {
        "name": "Langdale to Gambier Island & Keats Island",
        "major": False,
        "route_number": 13,
        "vessel_tracking": None
    },
    {
        "name": "Comox - Powell River (Little River-Westview)",
        "major": False,
        "route_number": 17,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route23.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route23.html"
        }
    },
    {
        "name": "Powell River - Texada Island (Westview-Blubber Bay)",
        "major": False,
        "route_number": 18,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route24.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route24.html",
           "top": 49.872070, 
           "right": -124.492607,
           "bottom": 49.763082, 
           "left": -124.656029
        }
    },
    {
        "name": "Nanaimo Harbour - Gabriola Island (Vancouver Island - Descanso Bay)",
        "major": False,
        "route_number": 19,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route19.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route19.html",
          "top": 49.228360, 
          "right": -123.816948,
          "bottom": 49.115456, 
          "left": -123.992386
        }
    },
    {
        "name": "Chemainus - Thetis Island - Penelakut Island",
        "major": False,
        "route_number": 20,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route18.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route18.html",
           "top": 49.024137, 
           "right": -123.609924,
           "bottom": 48.914265, 
           "left": -123.780212
        }
    },
    {
        "name": "Vancouver Island - Denman Island (Buckley Bay - Denman West)",
        "major": False,
        "route_number": 21,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route20.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route20.html",
          "vessel": "Baynes Sound Connector"
        }
    },
    {
        "name": "Denman Island - Hornby Island (Gravelly Bay-Shingle Spit)",
        "major": False,
        "route_number": 22,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route20.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route20.html"
        }
    },
    {
        "name": "Campbell River - Quadra Island (Quathiaski Cove)",
        "major": False,
        "route_number": 23,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route21.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route21.html"
        }
    },
    {
        "name": "Quadra Island - Cortes Island (Heriot Bay-Whaletown)",
        "major": False,
        "route_number": 24,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route22.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route22.html",
          "top": 50.092393, 
          "right": -125.143032,
          "bottom": 49.983351, 
          "left": -125.312805
        }
    },
    {
        "name": "Port McNeill - Alert Bay - Sointula (Vancouver Island-Cormorant Island-Malcolm Island)",
        "major": False,
        "route_number": 25,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route25.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route25.html",
          "top": 50.560123, 
          "right": -126.925907,
          "bottom": 50.669484, 
          "left": -127.093964
        }
    },
    {
        "name": "Alliford Bay - Skidegate (Moresby Island-Graham Island)",
        "major": False,
        "route_number": 26,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.html"
        }
    },
    {
        "name": "Inside Passage",
        "major": False,
        "route_number": 28,
        "vessel_tracking": {
          "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.jpg",
          "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route13.html"
        }
    },
    {
        "name": "Vancouver - Nanaimo (Tsawwassen-Duke Point)",
        "major": True,
        "route_number": 30,
        "vessel_tracking": {
            "image_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route1.jpg",
            "page_url": "https://apigateway.bcferries.com/api/currentconditions/1.0/images/vessels/route1.html",
            "top": 49.670018, 
            "right": -122.910209,
            "bottom": 48.782737, 
            "left": -124.271125
        }
    }
]

def get_route_number(route_name):
    for bcf_route in bcf_routes:
        if route_name in bcf_route["name"]:
            return bcf_route["route_number"]
    return '???'

class VesselInfo:
    def __init__(self, name, status, destination, route):
        self.name = name
        self.status = status
        self.destination = destination
        self.route_number = route["route_number"]
        self.route_name = route["name"]
        self.is_major = route['major']
        self.x = None
        self.y = None
        self.lon = None
        self.lat = None
        self.speed = None
        self.heading = None
        self.tracked_time = datetime.now()
        
    @classmethod
    def from_tr_soup(cls, tr_soup, route_dict):
        tds = tr_soup.find_all('td')
        return cls(
            name=tds[0].string, 
            status=tds[1].string,
            destination=tds[2].string,
            route=route_dict
        )
        
def scrape_vessel_info(html, route):
    """
    For reference, the relevant section
    <div id="vessel_status" style="width: 500px; background-color: White; ">
		<table style="width: 100%; font: 11px Verdana, sans-serif;">
			<tr>
				<td style="border-bottom: solid 1px black;"><b>Vessel</b></td>
				<td style="border-bottom: solid 1px black;"><b>Status</b></td>
				<td style="border-bottom: solid 1px black;"><b>Destination</b></td>
				<td style="border-bottom: solid 1px black;"><b>Last Update</b></td>
			</tr>
			<tr>
				<td>Queen of Alberni</td>
				<td>Under Way</td>
				<td>Tsawwassen</td>
				<td>0:18 AM</td>
			</tr>
			<tr>
				<td>Coastal Inspiration</td>
				<td>Under Way</td>
				<td>Duke Point</td>
				<td>0:18 AM</td>
			</tr>
		<tr><td colspan='4'>&nbsp;</td></tr>
		<tr><td colspan='4'><i>Each arrow icon <IMG SRC='images/icon1.gif' WIDTH='14' HEIGHT='14'/ > represents one of our vessels.  To view vessel name, destination, heading and speed, move your cursor over the arrow icon.  When <IMG SRC='images/icon0.gif' WIDTH='14' HEIGHT='14'/ > is displayed, the ship is in port.  Vessels not appearing on this map are either not yet in operation or are temporarily off line.</i></td></tr>
		</table>
	</div>
    """
    soup = BeautifulSoup(html, features="lxml")
    
    vessel_status_div = soup.find(id="vessel_status")
    vessel_status_table = vessel_status_div.table
    vessel_rows = vessel_status_div.find_all('tr')
    if len(vessel_rows) < 2:
        return []
    # Manually specified scrape to get the correct rows only, see example
    legit_vessel_rows = [vr for vr in vessel_rows[1:] if len(vr.find_all('td')) == 4]
    return [VesselInfo.from_tr_soup(tr, route) for tr in legit_vessel_rows]
    
def scrape_vessel_positions(html):
    """
    Example code from which we will get pixel coords:
    Some lines skipped for brevity
    
    function onMapHover(e) {
	getMouseXY(e);
    ...
	if (x >= 163 && y >= 441 && x <= 177 && y <= 455) {
		if (infoBoxShowing != 2) {
			...
			ferryInfo.style.left = 187;
			ferryInfo.style.top = 286;
			...
			infoBoxShowing = 2;
		}
	} else 	if (x >= 366 && y >= 91 && x <= 380 && y <= 105) {
		...
		}
	} else 	if (x >= 165 && y >= 441 && x <= 179 && y <= 455) {
		...
		}
	} else {
	   ...
	}
}

    So we can see its checking mouse coords for each boat. 
    
    """
    
    # This approach is presumptious and reckless but bold
    # remove everything but some punctuation and newlines
    filtered_html = re.sub('[^\(\)><=&\n]', '', html)
    filtered_lines = filtered_html.split('\n') # rely on file having newlines
    numbers_only = re.sub('[^ 0-9\n]', '', html).split('\n')
    
    vessel_pixel_tuples = []
    
    for idx, line in enumerate(filtered_lines):
        # Yes. Yes, my child. I am serious. We did go there.
        if '(>=&&>=&&<=&&<=)' in line:
            # so for each vessel
            nums = numbers_only[idx].split()
            # take avg of icon bounds
            x = (int(nums[2]) + int(nums[0])) / 2 
            y = (int(nums[3]) + int(nums[1])) / 2
            vessel_pixel_tuples.append((x, y))
            
    return vessel_pixel_tuples
            
    
def scrape_vessel_heading_and_speed(html):
    '''
    Example:
    
    	html += '</tr>';
			html += '<tr>';
			html += '<td>Heading: <b>NE</b></td>';
			html += '</tr>';
			html += '<tr>';
			html += '<td>Speed: <b>0 knots</b></td>';
			html += '</tr>';
    
    '''
    # grab heading/speed values in the same order as positions and info
    
    numbers_only_lines = re.sub('[^. 0-9\n]', '', html).split('\n')
    
    vessel_headings = []
    vessel_speeds = []
    
    for idx, line in enumerate(html.split('\n')):
        if 'Heading: <b>' in line:
            heading = line.split('<b>')[1].split('</b>')[0]
            vessel_headings.append(heading)
        
        if 'Speed: <b>' in line:
            speed = numbers_only_lines[idx]
            vessel_speeds.append(float(speed))
    
    return list(zip(vessel_headings, vessel_speeds))


def xy_to_latlon(x, y, route):
    """
       Very unfortunate. I manually guessed the lat lon limits of the
       map views using gmaps to compare. 
       
       We can use math to interpolate the pixel coords into real latlons
    """
    IMG_X_SIZE = 500
    IMG_Y_SIZE = 500
    
    top = route["vessel_tracking"]["top"]
    bottom = route["vessel_tracking"]["bottom"]
    left = route["vessel_tracking"]["left"]
    right = route["vessel_tracking"]["right"]
    
    frac_x = x / IMG_X_SIZE # fraction of pixel distance from left to right
    frac_y = y / IMG_Y_SIZE
    
    lat_size = top - bottom
    lon_size = right - left
    
    frac_lat = lat_size * frac_y # fraction of lat distance, bottom to top
    frac_lon = lon_size * frac_x
    
    final_lat = top - frac_lat # image pixels count down from the top, remember
    final_lon = left + frac_lon
    
    CONST_LAT_CORRECTION = 0 # 0.0032 # looks like we're always a bit too far south
    CONST_LON_CORRECTION = -0.002 # looks like we're always a bit east
    
    return final_lat + CONST_LAT_CORRECTION, final_lon + CONST_LON_CORRECTION
    
    
def scrape():
    all_vessel_infos = []
    for route in bcf_routes:
        if "vessel_tracking" not in route or route["vessel_tracking"] is None:
            continue
        page_url = route["vessel_tracking"]["page_url"]
        print(f'\nscraping: {route["route_number"]} {route["name"]} --- --- ---')
        try:
            html = requests.get(page_url).text # sync, ASGI would help
        except requests.exceptions.ConnectionError:
            print(f'BCF: SCRAPE: Connection error on route {route["route_number"]}!!! Skipping.')
            continue
        vessels = scrape_vessel_info(html, route)
        vessel_pos_list = scrape_vessel_positions(html)
        vessel_hdg_speed_list = scrape_vessel_heading_and_speed(html)
        
        # now, associate the positions with the boats. offline boats
        # have no pos data so must skip them
        i = -1
        for vessel in vessels:
            if vessel.status == 'Temporarily Off Line':
                continue
            i += 1
            vessel.x = vessel_pos_list[i][0]
            vessel.y = vessel_pos_list[i][1]
            
            vessel.heading = vessel_hdg_speed_list[i][0]
            vessel.speed = vessel_hdg_speed_list[i][1]
            
            # check needed if not all images have their coords yet
            if "vessel_tracking" in route and "top" in route["vessel_tracking"]:
                lat, lon = xy_to_latlon(vessel.x, vessel.y, route)
                vessel.lat = lat
                vessel.lon = lon
            
            all_vessel_infos.append(vessel)
            
        # just for printing
        for vessel in vessels:
            if vessel.status == 'Temporarily Off Line':
                print(f'--> {vessel.name}: {vessel.status} on {vessel.route_number} to {vessel.destination}')
                continue
            if vessel.lat is not None:
                print(f'--> {vessel.name}: {vessel.status} on {vessel.route_number} to {vessel.destination} at {vessel.lat}, {vessel.lon} hdg: {vessel.heading} spd: {vessel.speed}')
                continue
            print(f'--> {vessel.name}: {vessel.status} on {vessel.route_number} to {vessel.destination} at pixels {vessel.y}, {vessel.x} hdg: {vessel.heading} spd: {vessel.speed}')
            
    
    return all_vessel_infos