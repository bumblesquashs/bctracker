
% import json

% is_preview = get('is_preview', True)

<div id="map" class="{{ 'preview' if is_preview else 'full-screen' }}"></div>

<script>
    const map = new mapboxgl.Map({
        container: "map",
        center: [0, 0],
        zoom: 1,
        style: mapStyle,
        interactive: "{{ is_preview }}" === "False"
    });
    
    const lats = [];
    const lons = [];
</script>

% if not is_preview:
    <script>
        map.addControl(
            new mapboxgl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true
                },
                trackUserLocation: true,
                showUserHeading: true
            }),
            'bottom-left'
        );
    </script>
% end

% map_trips = get('map_trips', [map_trip] if defined('map_trip') and map_trip is not None else [])
% map_trips = sorted([t for t in map_trips if t.route is not None], key=lambda t: t.route, reverse=True)
% shape_ids = set()
% shape_trips = []
% for trip in map_trips:
    % if trip.shape_id not in shape_ids:
        % shape_ids.add(trip.shape_id)
        % shape_trips.append(trip)
    % end
% end
% if len(shape_trips) > 0:
    <script>
        const trips = JSON.parse('{{! json.dumps([t.get_json() for t in shape_trips]) }}');
        
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
                
                if ("{{ get('zoom_trips', True) }}" === "True") {
                    for (const point of trip.points) {
                        lats.push(point.lat);
                        lons.push(point.lon);
                    }
                }
            }
        });
    </script>
% end

% map_departures = get('map_departures', [map_departure] if defined('map_departure') and map_departure is not None else [])
% map_departures = sorted([d for d in map_departures if d.trip is not None and d.trip.route is not None], key=lambda d: d.trip.route)
% stop_ids = set()
% stop_departures = []
% for departure in map_departures:
    % if departure.stop_id not in stop_ids:
        % stop_ids.add(departure.stop.id)
        % stop_departures.append(departure)
    % end
% end
% if len(stop_departures) > 0:
    <script>
        const departures = JSON.parse('{{! json.dumps([d.get_json() for d in stop_departures]) }}');
        
        for (const departure of departures) {
            const stop = departure.stop;
            
            const element = document.createElement("div");
            element.className = "{{ 'marker' if len(map_departures) == 1 else 'marker small' }}";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = getUrl(stop.system_id, "stops/" + stop.number);
            icon.style.backgroundColor = "#" + departure.colour;
            icon.innerHTML = "<div class='link'></div><img src='/img/white/stop.png' />";
            
            const details = document.createElement("div");
            details.className = "details {{ '' if len(map_departures) == 1 else 'hover-only' }}";
            
            const title = document.createElement("div");
            title.className = "title";
            title.innerHTML = stop.number;
            
            const content = document.createElement("div");
            content.classList = "content hover-only centred";
            let routesHTML = "";
            for (const route of stop.routes) {
                routesHTML += "<span class='route' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
            }
            content.innerHTML = stop.name + "<div>" + routesHTML + "</div>";
            
            details.appendChild(title);
            details.appendChild(content);
            
            element.appendChild(icon);
            element.appendChild(details);
            
            new mapboxgl.Marker(element).setLngLat([stop.lon, stop.lat]).addTo(map);
            
            if ("{{ get('zoom_departures', True) }}" === "True") {
                lats.push(stop.lat);
                lons.push(stop.lon);
            }
        }
    </script>
% end

% map_stops = get('map_stops', [map_stop] if defined('map_stop') and map_stop is not None else [])
% if len(map_stops) > 0:
    <script>
        const stops = JSON.parse('{{! json.dumps([s.get_json() for s in map_stops]) }}');
        
        for (const stop of stops) {
            const element = document.createElement("div");
            element.className = "{{ 'marker' if len(map_stops) == 1 else 'marker small' }}";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = getUrl(stop.system_id, "stops/" + stop.number);
            icon.innerHTML = "<div class='link'></div><img src='/img/white/stop.png' />";
            
            const details = document.createElement("div");
            details.className = "details {{ '' if len(map_stops) == 1 else 'hover-only' }}";
            
            const title = document.createElement("div");
            title.className = "title";
            title.innerHTML = stop.number;
            
            const content = document.createElement("div");
            content.classList = "content hover-only centred";
            let routesHTML = "";
            for (const route of stop.routes) {
                routesHTML += "<span class='route' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
            }
            content.innerHTML = stop.name + "<div>" + routesHTML + "</div>";
            
            details.appendChild(title);
            details.appendChild(content);
            
            element.appendChild(icon);
            element.appendChild(details);
            
            new mapboxgl.Marker(element).setLngLat([stop.lon, stop.lat]).addTo(map);
            
            if ("{{ get('zoom_stops', True) }}" === "True") {
                lats.push(stop.lat);
                lons.push(stop.lon);
            }
        }
    </script>
% end

% map_positions = get('map_positions', [map_position] if defined('map_position') and map_position is not None else [])
% if len(map_positions) > 0:
    % map_positions = sorted([p for p in map_positions if p.has_location], key=lambda p: p.lat, reverse=True)
    <script>
        const positions = JSON.parse('{{! json.dumps([p.get_json() for p in map_positions]) }}');
        const busMarkerStyle = "{{ bus_marker_style }}";
        
        for (const position of positions) {
            const element = document.createElement("div");
            element.className = "marker";
            if (position.bearing !== undefined) {
                const sideWidthValue = busMarkerStyle == "mini" ? 8 : 16;
                const bottomWidthValue = busMarkerStyle == "mini" ? 18 : 26;
                const length = Math.floor(position.speed / 10);
                const bearing = document.createElement("div");
                bearing.className = "bearing";
                bearing.style.borderBottomColor = "#" + position.colour;
                bearing.style.marginTop = (-8 - length) + "px";
                bearing.style.borderLeftWidth = sideWidthValue + "px";
                bearing.style.borderRightWidth = sideWidthValue + "px";
                bearing.style.borderBottomWidth = (bottomWidthValue + length) + "px";
                bearing.style.transform = "rotate(" + position.bearing + "deg)";
                element.appendChild(bearing)
            }
            
            const details = document.createElement("div");
            details.className = "details";
            
            const title = document.createElement("div");
            title.className = "title";
            title.innerHTML = position.bus_display;
            
            const content = document.createElement("div");
            content.className = "content hover-only";
            
            const model = document.createElement("div");
            model.className = "lighter-text centred";
            model.innerHTML = position.bus_order;
            content.appendChild(model);
            
            const headsign = document.createElement("div");
            if (position.adherence !== null && position.adherence !== undefined) {
                headsign.className = "row center gap-5";
                const adherence = position.adherence;
                const adherenceElement = document.createElement("div");
                adherenceElement.classList.add("adherence");
                adherenceElement.classList.add(adherence.status_class);
                adherenceElement.innerHTML = adherence.value;
                
                headsign.innerHTML = adherenceElement.outerHTML + position.headsign;
            } else {
                headsign.className = "centred";
                headsign.innerHTML = position.headsign;
            }
            content.appendChild(headsign);
            
            if ("{{ system is None }}" === "True") {
                const system = document.createElement("div");
                system.className = "lighter-text centred";
                system.innerHTML = position.system;
                content.appendChild(system);
            }
            
            if (position.bus_number < 0) {
                const icon = document.createElement("div");
                icon.className = "icon";
                icon.style.backgroundColor = "#" + position.colour;
                if (busMarkerStyle == "route") {
                    icon.classList.add("bus_route");
                    icon.innerHTML = position.route_number;
                } else if (busMarkerStyle == "mini") {
                    element.classList.add("small");
                    icon.classList.add("mini");
                } else {
                    icon.innerHTML = "<img src='/img/white/" + position.bus_icon + ".png' />";
                }
                element.appendChild(icon);
            } else {
                const icon = document.createElement("a");
                icon.className = "icon";
                icon.href = "/bus/" + position.bus_number;
                icon.style.backgroundColor = "#" + position.colour;
                if (busMarkerStyle == "route") {
                    icon.classList.add("bus_route");
                    icon.innerHTML = "<div class='link'></div>" + position.route_number;
                } else if (busMarkerStyle == "mini") {
                    element.classList.add("small");
                    icon.classList.add("mini");
                    icon.innerHTML = "<div class='link'></div>";
                } else {
                    icon.innerHTML = "<div class='link'></div><img src='/img/white/" + position.bus_icon + ".png' />";
                }
                element.appendChild(icon);
            }
            
            if (position.adornment != null) {
                title.innerHTML += " <span class='adornment'>" + position.adornment + "</span>";
            }
            
            details.appendChild(title);
            details.appendChild(content);
            element.appendChild(details);
            
            new mapboxgl.Marker(element).setLngLat([position.lon, position.lat]).addTo(map);
            
            if ("{{ get('zoom_buses', True) }}" === "True" && position.lat != 0 && position.lon != 0) {
                lats.push(position.lat);
                lons.push(position.lon);
            }
        }
    </script>
% end

<script>
    map.on("load", function() {
        map.resize();
        if (lons.length === 1 && lats.length === 1) {
            map.jumpTo({
                center: [lons[0], lats[0]],
                zoom: 14
            });
        } else if (lons.length > 0 && lats.length > 0) {
            const minLon = Math.min.apply(Math, lons);
            const maxLon = Math.max.apply(Math, lons);
            const minLat = Math.min.apply(Math, lats);
            const maxLat = Math.max.apply(Math, lats);
            
            map.fitBounds([[minLon, minLat], [maxLon, maxLat]], {
                duration: 0,
                padding: parseInt("{{ 20 if is_preview else 100 }}")
            });
        }
    });
</script>
