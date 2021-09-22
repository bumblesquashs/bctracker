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
    <div id="system-map-header" class="page-header">
        <h1 class="title">Map</h1>
        <div class="checkbox" onclick="toggleTripLines()">
            <div class="box">
                <img class="hidden" id="checkbox-image" src="/img/check.png" />
            </div>
            <span class="checkbox-label">Show Route Lines</span>
        </div>
        <div class="checkbox" onclick="toggleAutomaticRefresh()">
            <div class="box">
                <img class="hidden" id="refresh-image" src="/img/check.png" />
            </div>
            <span class="checkbox-label">Automatically Refresh</span>
        </div>
    </div>
    
    <div id="system-map"></div>
    
    <script>
        const map = new mapboxgl.Map({
            container: "system-map",
            center: [0, 0],
            zoom: 1,
            style: prefersDarkScheme ? "mapbox://styles/mapbox/dark-v10" : "mapbox://styles/mapbox/light-v10"
        });
        
        let buses = JSON.parse('{{! json.dumps([b.json_data for b in buses if b.position.has_location]) }}');
        let current_shape_ids = []
        let markers = [];
        let tripLinesVisible = false;
        let automaticRefresh = false;
        
        const shape_ids = [];
        
        map.on("load", function() {
            updateMap(true);
        })
        
        function updateMap(resetPosition) {
            current_shape_ids = []
            for (const marker of markers) {
                marker.remove();
            }
            markers = [];
            
            const lons = [];
            const lats = [];
            
            for (const bus of buses) {
                if (bus.shape_id !== null && bus.shape_id !== undefined) {
                    if (!(current_shape_ids.includes(bus.shape_id))) {
                        current_shape_ids.push(bus.shape_id)
                    }
                }
                
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
        
                markers.push(new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map));
            }
            
            if (resetPosition) {
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
            }
            
            for (const shape_id of shape_ids) {
                if (current_shape_ids.includes(shape_id)) {
                    map.setLayoutProperty(shape_id, "visibility", tripLinesVisible ? "visible" : "none");
                } else {
                    map.setLayoutProperty(shape_id, "visibility", "none");
                }
            }
        }
        
        function toggleTripLines() {
            tripLinesVisible = !tripLinesVisible;
            const checkboxImage = document.getElementById("checkbox-image");
            checkboxImage.classList.toggle("hidden");
            
            for (const shape_id of current_shape_ids) {
                if (shape_ids.includes(shape_id)) {
                    map.setLayoutProperty(shape_id, "visibility", tripLinesVisible ? "visible" : "none");
                }
            }
            if (tripLinesVisible) {
                updateRouteData()
            }
        }
        
        function toggleAutomaticRefresh() {
            automaticRefresh = !automaticRefresh;
            const checkboxImage = document.getElementById("refresh-image");
            checkboxImage.classList.toggle("hidden");
            
            if (automaticRefresh) {
                updateBusData()
            }
        }
        
        function updateBusData() {
            const request = new XMLHttpRequest();
            request.open("GET", "{{get_url(system, 'api/map.json')}}", true);
            request.responseType = "json";
            request.onload = function() {
                if (request.status === 200) {
                    const lastUpdated = request.response.last_updated;
                    const element = document.getElementById("last-updated");
                    if (element !== null && element !== undefined && element.innerHTML.trim() !== "Updated " + lastUpdated) {
                        element.innerHTML = "Updated " + lastUpdated;
                        buses = request.response.buses;
                        updateMap(false);
                        if (tripLinesVisible) {
                            updateRouteData()
                        }
                    }
                }
            };
            request.send();
        }
        
        function updateRouteData() {
            for (const bus of buses) {
                if (bus.shape_id === null || bus.shape_id === undefined) {
                    continue;
                }
                if (shape_ids.includes(bus.shape_id)) {
                    continue;
                } else {
                    shape_ids.push(bus.shape_id);
                }
                const request = new XMLHttpRequest();
                request.open("GET", "/" + bus.system_id + "/api/shape/" + bus.shape_id + ".json", true);
                request.responseType = "json";
                request.onload = function() {
                    if (request.status === 200) {
                        map.addSource(bus.shape_id, {
                            'type': 'geojson',
                            'data': {
                                'type': 'Feature',
                                'properties': {},
                                'geometry': {
                                    'type': 'LineString',
                                    'coordinates': request.response.points.map(function (point) { return [point.lon, point.lat] })
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
                                'visibility':  tripLinesVisible ? 'visible' : 'none'
                            },
                            'paint': {
                                'line-color': '#' + bus.colour,
                                'line-width': 4
                            }
                        });
                    }
                };
                request.send();
            }
        }
        
        const date = new Date();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        const timeSinceLastUpdate = ((minutes % 2) * 60) + seconds;
        const timeToNextUpdate = (2 * 60) - timeSinceLastUpdate;
        
        setTimeout(function() {
            if (automaticRefresh) {
                updateBusData();
            }
            setInterval(function() {
                if (automaticRefresh) {
                    updateBusData();
                }
            }, 1000 * 60 * 2);
        }, 1000 * (timeToNextUpdate + 15));
    </script>
% end
