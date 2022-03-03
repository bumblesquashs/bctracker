
% import json

% is_preview = get('is_preview', True)

<div id="map" class="{{ 'preview' if is_preview else 'full-screen' }}"></div>

<script>
    const map = new mapboxgl.Map({
        container: "map",
        center: [0, 0],
        zoom: 1,
        style: prefersDarkScheme ? "mapbox://styles/mapbox/dark-v10" : "mapbox://styles/mapbox/light-v10",
        interactive: "{{ is_preview }}" === "False"
    });
    
    const lats = [];
    const lons = [];
</script>

% map_trips = get('map_trips', [map_trip] if defined('map_trip') and map_trip is not None else [])
% map_trips = sorted(map_trips, key=lambda t: t.route, reverse=True)
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
% map_departures = sorted(map_departures, key=lambda d: d.trip.route)
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
        const departures = JSON.parse('{{! json.dumps([d.json_data for d in stop_departures]) }}');
        
        for (const departure of departures) {
            const stop = departure.stop;
            
            const element = document.createElement("div");
            element.className = "{{ 'marker' if len(map_departures) == 1 else 'marker small' }}";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = getUrl(stop.system_id, "stops/" + stop.number);
            icon.style.backgroundColor = "#" + departure.colour;
            icon.innerHTML = "<div class='link'></div><img src='/img/white/stop.png' />";
            
            let routesHTML = "";
            for (const route of stop.routes) {
                routesHTML += "<span class='route-number' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
            }
            
            const details = document.createElement("div");
            details.className = "details";
            details.innerHTML = "\
                <div class='{{ 'title' if len(map_departures) == 1 else 'title hover-only' }}'>" + stop.number + "</div>\
                <div class='subtitle hover-only'>" + stop.name + "</div>\
                <div class='subtitle hover-only'>" + routesHTML + "</div>";
            
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
        const stops = JSON.parse('{{! json.dumps([s.json_data for s in map_stops]) }}');
        
        for (const stop of stops) {
            const element = document.createElement("div");
            element.className = "{{ 'marker' if len(map_stops) == 1 else 'marker small' }}";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = getUrl(stop.system_id, "stops/" + stop.number);
            icon.innerHTML = "<div class='link'></div><img src='/img/white/stop.png' />";
            
            let routesHTML = "";
            for (const route of stop.routes) {
                routesHTML += "<span class='route-number' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
            }
            
            const details = document.createElement("div");
            details.className = "details";
            details.innerHTML = "\
                <div class='{{ 'title' if len(map_stops) == 1 else 'title hover-only' }}'>" + stop.number + "</div>\
                <div class='subtitle hover-only'>" + stop.name + "</div>\
                <div class='subtitle hover-only'>" + routesHTML + "</div>";
            
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

% map_buses = get('map_buses', [map_bus] if defined('map_bus') and map_bus is not None else [])
% if len(map_buses) > 0:
    <script>
        const buses = JSON.parse('{{! json.dumps([b.json_data for b in map_buses]) }}');
        
        for (const bus of buses) {
            const adherenceElement = document.createElement("span")
            if (bus.schedule_adherence !== null && bus.schedule_adherence !== undefined) {
                const adherence = bus.schedule_adherence
                adherenceElement.classList.add("adherence-indicator")
                adherenceElement.classList.add(adherence.status_class)
                adherenceElement.innerHTML = adherence.value
            }
            const element = document.createElement("div");
            element.className = "marker";
            if (bus.number < 0) {
                const icon = document.createElement("div");
                icon.className = "icon";
                icon.style.backgroundColor = "#" + bus.colour;
                icon.innerHTML = "<img src='/img/bus.png' />";
                
                const details = document.createElement("div");
                details.className = "details";
                details.innerHTML = "\
                    <div class='title'>Unknown Bus</div>\
                    <div class='subtitle hover-only'>" + adherenceElement.outerHTML + bus.headsign + "</div>"
                
                element.appendChild(icon);
                element.appendChild(details);
            } else {
                const icon = document.createElement("a");
                icon.className = "icon";
                icon.href = "/bus/" + bus.number;
                icon.style.backgroundColor = "#" + bus.colour;
                icon.innerHTML = "<div class='link'></div><img src='/img/bus.png' />";
                
                const details = document.createElement("div");
                details.className = "details";
                details.innerHTML = "\
                    <div class='title'>" + bus.number + "</div>\
                    <div class='subtitle hover-only'>" + adherenceElement.outerHTML + bus.headsign + "</div>";
                
                element.appendChild(icon);
                element.appendChild(details);
            }
            
            new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map);
            
            if ("{{ get('zoom_buses', True) }}" === "True") {
                lats.push(bus.lat);
                lons.push(bus.lon);
            }
        }
    </script>
% end

<script>
    map.on("load", function() {
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
                    top: parseInt("{{ 20 if is_preview else 200 }}"),
                    bottom: parseInt("{{ 20 if is_preview else 100 }}"),
                    left: parseInt("{{ 20 if is_preview else 100 }}"),
                    right: parseInt("{{ 20 if is_preview else 100 }}")
                }
            });
        }
    });
</script>
