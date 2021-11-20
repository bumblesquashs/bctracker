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
    <div class="page-header map-page">
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
    
    <div id="map" class="full-screen"></div>
    
    <script>
        const map = new mapboxgl.Map({
            container: "map",
            center: [0, 0],
            zoom: 1,
            style: prefersDarkScheme ? "mapbox://styles/mapbox/dark-v10" : "mapbox://styles/mapbox/light-v10"
        });
        
        let buses = JSON.parse('{{! json.dumps([b.json_data for b in buses if b.position.has_location]) }}');
        let currentShapeIDs = []
        let markers = [];
        let tripLinesVisible = false;
        let automaticRefresh = false;
        let hoverBus = null
        
        const shapeIDs = [];
        
        map.on("load", function() {
            updateMap(true);
        })
        
        function updateMap(resetPosition) {
            currentShapeIDs = []
            for (const marker of markers) {
                marker.remove();
            }
            markers = [];
            
            const lons = [];
            const lats = [];
            
            for (const bus of buses) {
                if (bus.shape_id !== null && bus.shape_id !== undefined) {
                    const shapeID = bus.system_id + "_" + bus.shape_id
                    if (!(currentShapeIDs.includes(shapeID))) {
                        currentShapeIDs.push(shapeID)
                    }
                }
                
                let adherenceElement = document.createElement("span")
                if (bus.schedule_adherence !== null && bus.schedule_adherence !== undefined) {
                    adherence = bus.schedule_adherence
                    adherenceElement.classList.add("adherence-indicator")
                    if (adherence <= -8) {
                        adherenceElement.classList.add("very-behind")
                    } else if (adherence <= -5) {
                        adherenceElement.classList.add("behind")
                    } else if (adherence >= 5) {
                        adherenceElement.classList.add("very-ahead")
                    } else if (adherence >= 3) {
                        adherenceElement.classList.add("ahead")
                    } else {
                        adherenceElement.classList.add("on-time")
                    }
                    if (adherence > 0) {
                        adherenceElement.innerHTML = "+" + adherence
                    } else {
                        adherenceElement.innerHTML = "" + adherence
                    }
                }
                
                const element = document.createElement("div");
                element.id = "bus-marker-" + bus.number
                element.className = "marker";
                if (bus.number < 0) {
                    element.innerHTML = "\
                        <div class='icon' style='background-color: #" + bus.colour + ";'>\
                            <img src='/img/bus.png' />\
                        </div>\
                        <div class='details'>\
                            <div class='title'>Unknown Bus</div>\
                            <div class='subtitle hover-only'>" + adherenceElement.outerHTML + bus.headsign + "</div>\
                        </div>";
                } else {
                    element.innerHTML = "\
                        <a href='/bus/" + bus.number +"' class='icon' style='background-color: #" + bus.colour + ";'>\
                            <div class='link'></div>\
                            <img src='/img/bus.png' />\
                        </a>\
                        <div class='details'>\
                            <div class='title'>" + bus.number + "</div>\
                            <div class='subtitle hover-only'>" + adherenceElement.outerHTML + bus.headsign + "</div>\
                        </div>";
                }
                
                element.onmouseenter = function() {
                    setHoverBus(bus);
                }
                element.onmouseleave = function() {
                    setHoverBus(null);
                }
                
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
            
            for (const shapeID of shapeIDs) {
                if (currentShapeIDs.includes(shapeID)) {
                    map.setLayoutProperty(shapeID, "visibility", tripLinesVisible ? "visible" : "none");
                } else {
                    map.setLayoutProperty(shapeID, "visibility", "none");
                }
            }
        }
        
        function toggleTripLines() {
            tripLinesVisible = !tripLinesVisible;
            const checkboxImage = document.getElementById("checkbox-image");
            checkboxImage.classList.toggle("hidden");
            
            for (const shapeID of currentShapeIDs) {
                if (shapeIDs.includes(shapeID)) {
                    map.setLayoutProperty(shapeID, "visibility", tripLinesVisible ? "visible" : "none");
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
                const shapeID = bus.system_id + "_" + bus.shape_id
                if (shapeIDs.includes(shapeID)) {
                    continue;
                }
                const request = new XMLHttpRequest();
                request.open("GET", getUrl(bus.system_id, "api/shape/" + bus.shape_id + ".json"), true);
                request.responseType = "json";
                request.onload = function() {
                    if (request.status === 200) {
                        shapeIDs.push(shapeID);
                        map.addSource(shapeID, {
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
                            'id': shapeID,
                            'type': 'line',
                            'source': shapeID,
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
        
        function setHoverBus(bus) {
            if (tripLinesVisible) {
                return
            }
            if (hoverBus !== null) {
                if (shapeIDs.includes(hoverBus.shape_id)) {
                    map.setLayoutProperty(hoverBus.shape_id, "visibility", "none");
                }
            }
            if (bus !== null) {
                if (bus.shape_id === null || bus.shape_id === undefined) {
                    return;
                }
                if (shapeIDs.includes(bus.shape_id)) {
                    map.setLayoutProperty(bus.shape_id, "visibility", "visible");
                } else {
                    const request = new XMLHttpRequest();
                    request.open("GET", "/" + bus.system_id + "/api/shape/" + bus.shape_id + ".json", true);
                    request.responseType = "json";
                    request.onload = function() {
                        if (request.status === 200) {
                            shapeIDs.push(bus.shape_id);
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
                                    'visibility': (hoverBus === bus) ? 'visible' : 'none'
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
            hoverBus = bus;
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
