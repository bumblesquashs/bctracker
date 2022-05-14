
% import json

% rebase('base', title='Routes', include_maps=True)

% if system is None:
    <div class="page-header">
        <h1 class="title">Routes</h1>
        <div class="tab-button-bar">
            <a href="{{ get_url(system, 'routes') }}" class="tab-button">List</a>
            <span class="tab-button current">Map</span>
        </div>
        <hr />
    </div>
    
    <p>
        Routes can only be viewed for individual systems.
        Please choose a system.
    </p>
    % include('components/systems')
% else:
    <div class="page-header map-page">
        <h1 class="title">Routes</h1>
        <div class="tab-button-bar">
            <a href="{{ get_url(system, 'routes') }}" class="tab-button">List</a>
            <span class="tab-button current">Map</span>
        </div>
    </div>
    
    % routes = system.get_routes()
    
    <div id="map" class="full-screen"></div>
    
    <script>
        const map = new mapboxgl.Map({
            container: "map",
            center: [0, 0],
            zoom: 1,
            style: prefersDarkScheme ? "mapbox://styles/mapbox/dark-v10" : "mapbox://styles/mapbox/light-v10",
            interactive: true
        });
        
        const lats = [];
        const lons = [];
    </script>
    
    % trips = sorted([t for r in routes for t in r.trips], key=lambda t: t.route, reverse=True)
    % shape_ids = set()
    % shape_trips = []
    % for trip in trips:
        % if trip.shape_id not in shape_ids:
            % shape_ids.add(trip.shape_id)
            % shape_trips.append(trip)
        % end
    % end
    
    % if len(shape_trips) > 0:
        <script>
            const trips = JSON.parse('{{! json.dumps([t.json_data for t in shape_trips]) }}');
            
            map.on("load", function() {
                for (const trip of trips) {
                    const shapeID = String(trip.shape_id);
                    map.addSource(shapeID, {
                        "type": "geojson",
                        "data": {
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                                "type": "LineString",
                                "coordinates": trip.points.map(function (point) { return [point.lon, point.lat] })
                            }
                        }
                    });
                    map.addLayer({
                        "id": shapeID,
                        "type": "line",
                        "source": shapeID,
                        "layout": {
                            "line-join": "round",
                            "line-cap": "round"
                        },
                        "paint": {
                            "line-color": "#" + trip.colour,
                            "line-width": 4
                        }
                    });
                    
                    for (const point of trip.points) {
                        lats.push(point.lat);
                        lons.push(point.lon);
                    }
                }
                if (lons.length === 1 && lats.length === 1) {
                    map.jumpTo({
                        center: [lons[0], lats[0]],
                        zoom: 14
                    });
                } else {
                    const minLon = Math.min.apply(Math, lons);
                    const maxLon = Math.max.apply(Math, lons);
                    const minLat = Math.min.apply(Math, lats);
                    const maxLat = Math.max.apply(Math, lats);
                    
                    map.fitBounds([[minLon, minLat], [maxLon, maxLat]], {
                        duration: 0,
                        padding: {
                            top: 200,
                            bottom: 100,
                            left: 100,
                            right: 100
                        }
                    });
                }
            });
        </script>
        
        % routes_json = [j for r in routes for j in r.indicator_json_data]
        <script>
            const routes = JSON.parse('{{! json.dumps(routes_json) }}');
            
            for (const route of routes) {
                const element = document.createElement("div");
                element.className = "marker";
                
                const icon = document.createElement("a");
                icon.className = "icon route";
                icon.href = getUrl(route.system_id, "routes/" + route.number);
                icon.style.backgroundColor = "#" + route.colour;
                icon.innerHTML = "<div class='link'></div><span class='number'>" + route.number + "</span>";
                
                const details = document.createElement("div");
                details.className = "details";
                details.innerHTML = "<div class='title hover-only'>" + route.name + "</div>";
                
                element.appendChild(icon);
                element.appendChild(details);
                
                new mapboxgl.Marker(element).setLngLat([route.lon, route.lat]).addTo(map);
            }
        </script>
    % end
    
    % include('components/map_z_toggle')  
% end
