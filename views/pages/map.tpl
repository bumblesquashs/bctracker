% import json

% rebase('base', title='Map', include_maps=True)

% if len(buses) == 0:
    <div class="page-header">
        <h1 class="title">Map</h1>
    </div>
    <hr />

    % if system is not None and not system.realtime_enabled:
        <p>
            {{ system }} does not currently support realtime.
            You can browse the schedule data for {{ system }} using the links above, or choose another system that supports realtime from the following list.
        </p>
        
        % include('components/systems', realtime_only=True)
    % else:
        % if system is None:
            <p>
                There are no buses out right now.
                BC Transit does not have late night service, so this should be the case overnight.
                If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.
                Please check back later!
            </p>
        % else:
            <p>
                There are no buses out in {{ system }} right now.
                Please choose a different system.
            </p>
            
            % include('components/systems', realtime_only=True)
        % end
    % end
% else:
    <div id="page-header system-map-header">
        <h1 class="title">Map</h1>
        <div class="checkbox" onclick="toggleTripLines()">
            <div class="box">
                <img class="hidden" id="checkbox-image" src="/img/check.png" />
            </div>
            <span class="checkbox-label">Show Route Lines</span>
        </div>
    </div>
    
    <div id="system-map"></div>
    
    <script>
        const map = new mapboxgl.Map({
            container: "system-map",
            center: [0, 0],
            zoom: 1,
            style: prefersDarkScheme ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v10'
        });
        
        const buses = JSON.parse('{{! json.dumps([b.json_data for b in buses if b.position.has_location]) }}');
        const shape_ids = [];
        
        const lons = [];
        const lats = [];
        
        for (let bus of buses) {
            const element = document.createElement("div");
            element.className = "marker";
            if (bus.number === "Unknown Bus") {
                element.innerHTML = "\
                    <img src=\"/img/bus.png\" />\
                    <div class='title'><span>" + bus.number + "</span></div>\
                    <div class='subtitle'><span>" + bus.headsign + "</span></div>";
            } else {
                element.innerHTML = "\
                    <div class='link'></div>\
                    <a href=\"/bus/" + bus.number +"\">\
                        <img src=\"/img/bus.png\" />\
                        <div class='title'><span>" + bus.number + "</span></div>\
                        <div class='subtitle'><span>" + bus.headsign + "</span></div>\
                    </a>";
            }
            element.style.backgroundColor = "#" + bus.colour;
        
            lons.push(bus.lon);
            lats.push(bus.lat);
        
            new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map);
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
                padding: {top: 200, bottom: 100, left: 100, right: 100}
            });
        }
        
        map.on("load", function() {
            for (var bus of buses) {
                if (bus.points === null || bus.points === undefined) {
                    continue;
                }
                if (shape_ids.includes(bus.shape_id)) {
                    continue;
                } else {
                    shape_ids.push(bus.shape_id);
                }
                map.addSource(bus.shape_id, {
                    'type': 'geojson',
                    'data': {
                        'type': 'Feature',
                        'properties': {},
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': bus.points.map(function (point) { return [point.lon, point.lat] })
                        }
                    }
                });
                map.addLayer({
                    'id': bus.shape_id,
                    'type': 'line',
                    'source': bus.shape_id,
                    'minzoom': 8,
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round',
                        'visibility': 'none'
                    },
                    'paint': {
                        'line-color': '#' + bus.colour,
                        'line-width': 4
                    }
                });
            }
        })
        
        let tripLinesVisible = false;
        
        function toggleTripLines() {
            tripLinesVisible = !tripLinesVisible;
            let checkboxImage = document.getElementById("checkbox-image");
            if (tripLinesVisible) {
                checkboxImage.className = "checkbox-image";
            } else {
                checkboxImage.className = "checkbox-image hidden";
            }
            
            for (var bus of buses) {
                if (bus.points === null || bus.points === undefined) {
                    continue;
                }
                map.setLayoutProperty(bus.shape_id, "visibility", tripLinesVisible ? "visible" : "none");
            }
        }
    </script>
% end
