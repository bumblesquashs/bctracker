
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

% trips = get('trips', [trip] if defined('trip') else [])
% if len(trips) > 0:
    <script>
        const trips = JSON.parse('{{! json.dumps([t.json_data for t in trips]) }}');
        const shapeIDs = [];
        
        map.on("load", function() {
            for (const trip of trips) {
                const shapeID = String(trip.shape_id);
                if (shapeIDs.includes(shapeID)) {
                    continue;
                } else {
                    shapeIDs.push(shapeID);
                }
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
                
                if ("{{ get('bound_trips', True) }}" === "True") {
                    for (const point of trip.points) {
                        lats.push(point.lat);
                        lons.push(point.lon);
                    }
                }
            }
        });
    </script>
% end

% stops = get('stops', [stop] if defined('stop') else [])
% if len(stops) > 0:
    <script>
        const stops = JSON.parse('{{! json.dumps([s.json_data for s in stops]) }}');
        
        for (const stop of stops) {
            const element = document.createElement("div");
            element.className = "marker small";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = "{{ get_url(system) }}/stops/" + stop.number;
            icon.innerHTML = "<div class='link'></div><img src='/img/stop.png' />";
            
            const details = document.createElement("div");
            details.className = "details";
            details.innerHTML = "\
                <div class='title hover-only'>" + stop.number + "</div>\
                <div class='subtitle hover-only'>" + stop.name + "</div>";
            
            element.appendChild(icon);
            element.appendChild(details);
            
            new mapboxgl.Marker(element).setLngLat([stop.lon, stop.lat]).addTo(map);
            
            if ("{{ get('bound_stops', True) }}" === "True") {
                lats.push(stop.lat);
                lons.push(stop.lon);
            }
        }
    </script>
% end

% buses = get('buses', [bus] if defined('bus') else [])
% if len(buses) > 0:
    <script>
        const buses = JSON.parse('{{! json.dumps([b.json_data for b in buses]) }}');
        
        for (const bus of buses) {
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
                    <div class='subtitle hover-only'>" + bus.headsign + "</div>"
                
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
                    <div class='subtitle hover-only'>" + bus.headsign + "</div>";
                
                element.appendChild(icon);
                element.appendChild(details);
            }
            
            new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map);
            
            if ("{{ get('bound_buses', True) }}" === "True") {
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
