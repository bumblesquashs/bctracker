
% import json

% rebase('base', title='Map', include_maps=True, full_map=True)

% if len(positions) == 0:
    <div class="page-header">
        <h1 class="title">Map</h1>
        <hr />
    </div>

    % if system is not None and not system.realtime_enabled:
        <p>
            {{ system }} does not currently support realtime.
            You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
        </p>
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
        % end
    % end
% else:
    <div class="page-header map-page">
        <h1 class="title">Map</h1>
        <div class="checkbox" onclick="toggleTripLines()">
            <div class="box">
                <div id="checkbox-image" class="hidden">
                    <img class="white" src="/img/white/check.png" />
                    <img class="black" src="/img/black/check.png" />
                </div>
            </div>
            <span class="checkbox-label">Show Route Lines</span>
        </div>
        <div class="checkbox" onclick="toggleAutomaticRefresh()">
            <div class="box">
                <div id="refresh-image" class="hidden">
                    <img class="white" src="/img/white/check.png" />
                    <img class="black" src="/img/black/check.png" />
                </div>
            </div>
            <span class="checkbox-label">Automatically Refresh</span>
        </div>
        <div class="checkbox" onclick="toggleNISBuses()">
            <div class="box">
                <div id="nis-image">
                    <img class="white" src="/img/white/check.png" />
                    <img class="black" src="/img/black/check.png" />
                </div>
            </div>
            <span class="checkbox-label">Show NIS Buses</span>
        </div>
    </div>
    
    <div id="map" class="full-screen"></div>
    
    <script>
        const map = new mapboxgl.Map({
            container: "map",
            center: [0, 0],
            zoom: 1,
            style: mapStyle
        });
        
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
        
        let positions = JSON.parse('{{! json.dumps([p.json for p in positions if p.has_location]) }}');
        let currentShapeIDs = [];
        let markers = [];
        let tripLinesVisible = false;
        let automaticRefresh = false;
        let showNISBuses = true;
        let hoverPosition = null;
        
        const shapeIDs = [];
        
        map.on("load", function() {
            map.resize();
            updateMap(true);
        })
        
        function updateMap(resetCoordinates) {
            currentShapeIDs = [];
            for (const marker of markers) {
                marker.remove();
            }
            markers = [];
            
            const lons = [];
            const lats = [];
            
            for (const position of positions) {
                if (position.shape_id !== null && position.shape_id !== undefined) {
                    const shapeID = position.system_id + "_" + position.shape_id;
                    if (!(currentShapeIDs.includes(shapeID))) {
                        currentShapeIDs.push(shapeID);
                    }
                }
                
                const adherenceElement = document.createElement("span")
                if (position.adherence !== null && position.adherence !== undefined) {
                    const adherence = position.adherence;
                    adherenceElement.classList.add("adherence-indicator");
                    adherenceElement.classList.add(adherence.status_class);
                    adherenceElement.innerHTML = adherence.value;
                }
                
                const element = document.createElement("div");
                element.id = "bus-marker-" + position.bus_number;
                element.className = "marker";
                if (position.shape_id === null || position.shape_id === undefined) {
                    element.classList.add("nis-bus");
                    if (!showNISBuses) {
                        element.classList.add("hidden");
                    }
                }
                if (position.bearing !== undefined) {
                    const bearing = document.createElement("div");
                    bearing.className = "bearing";
                    bearing.style.borderBottomColor = "#" + position.colour;
                    bearing.style.transform = "rotate(" + position.bearing + "deg)";
                    element.appendChild(bearing)
                }
                if (position.bus_number < 0) {
                    const icon = document.createElement("div");
                    icon.className = "icon";
                    icon.style.backgroundColor = "#" + position.colour;
                    icon.innerHTML = "<img src='/img/white/bus.png' />";
                    
                    icon.onmouseenter = function() {
                        setHoverPosition(position);
                    }
                    icon.onmouseleave = function() {
                        setHoverPosition(null);
                    }
                    
                    const details = document.createElement("div");
                    details.className = "details";
                    details.innerHTML = "\
                        <div class='title'>Unknown Bus</div>\
                        <div class='subtitle hover-only'>" + adherenceElement.outerHTML + position.headsign + "</div>";
                    
                    element.appendChild(icon);
                    element.appendChild(details);
                } else {
                    const icon = document.createElement("a");
                    icon.className = "icon";
                    icon.href = "/bus/" + position.bus_number;
                    icon.style.backgroundColor = "#" + position.colour;
                    icon.innerHTML = "<div class='link'></div><img src='/img/white/bus.png' />";
                    
                    icon.onmouseenter = function() {
                        setHoverPosition(position);
                    }
                    icon.onmouseleave = function() {
                        setHoverPosition(null);
                    }
                    
                    const details = document.createElement("div");
                    details.className = "details";
                    details.innerHTML = "\
                        <div class='title'>" + position.bus_number + "</div>\
                        <div class='subtitle hover-only'>" + adherenceElement.outerHTML + position.headsign + "</div>";
                    
                    element.appendChild(icon);
                    element.appendChild(details);
                }
                
                if (position.lat != 0 && position.lon != 0) {
                    lons.push(position.lon);
                    lats.push(position.lat);
                }
                
                markers.push(new mapboxgl.Marker(element).setLngLat([position.lon, position.lat]).addTo(map));
            }
            
            if (resetCoordinates) {
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
                        padding: 100
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
                updateRouteData();
            }
        }
        
        function toggleAutomaticRefresh() {
            automaticRefresh = !automaticRefresh;
            const checkboxImage = document.getElementById("refresh-image");
            checkboxImage.classList.toggle("hidden");
            
            if (automaticRefresh) {
                updatePositionData();
            }
        }
        
        function toggleNISBuses() {
            showNISBuses = !showNISBuses;
            const checkboxImage = document.getElementById("nis-image");
            checkboxImage.classList.toggle("hidden");
            
            for (const element of document.getElementsByClassName("nis-bus")) {
                if (showNISBuses) {
                    element.classList.remove("hidden");
                } else {
                    element.classList.add("hidden");
                }
            }
        }
        
        function updatePositionData() {
            const request = new XMLHttpRequest();
            request.open("GET", "{{get_url(system, 'api/map.json')}}", true);
            request.responseType = "json";
            request.onload = function() {
                if (request.status === 200) {
                    const lastUpdated = request.response.last_updated;
                    const element = document.getElementById("last-updated");
                    if (element !== null && element !== undefined && element.innerHTML.trim() !== "Updated " + lastUpdated) {
                        element.innerHTML = "Updated " + lastUpdated;
                        positions = request.response.positions;
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
            for (const position of positions) {
                if (position.shape_id === null || position.shape_id === undefined) {
                    continue;
                }
                const shapeID = position.system_id + "_" + position.shape_id
                if (shapeIDs.includes(shapeID)) {
                    continue;
                }
                const request = new XMLHttpRequest();
                request.open("GET", getUrl(position.system_id, "api/shape/" + position.shape_id + ".json"), true);
                request.responseType = "json";
                request.onload = function() {
                    if (request.status === 200) {
                        if (shapeIDs.includes(shapeID)) {
                            map.setLayoutProperty(shapeID, "visibility", "visible");
                        } else {
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
                                    'line-color': '#' + position.colour,
                                    'line-width': 4
                                }
                            });
                        }
                    }
                };
                request.send();
            }
        }
        
        function setHoverPosition(position) {
            if (tripLinesVisible) {
                return
            }
            if (hoverPosition !== null) {
                const shapeID = hoverPosition.system_id + "_" + hoverPosition.shape_id
                if (shapeIDs.includes(shapeID)) {
                    map.setLayoutProperty(shapeID, "visibility", "none");
                }
            }
            if (position !== null) {
                if (position.shape_id === null || position.shape_id === undefined) {
                    return;
                }
                const shapeID = position.system_id + "_" + position.shape_id
                if (shapeIDs.includes(shapeID)) {
                    map.setLayoutProperty(shapeID, "visibility", "visible");
                } else {
                    const request = new XMLHttpRequest();
                    request.open("GET", getUrl(position.system_id, "api/shape/" + position.shape_id + ".json"), true);
                    request.responseType = "json";
                    request.onload = function() {
                        if (request.status === 200) {
                            if (shapeIDs.includes(shapeID)) {
                                map.setLayoutProperty(shapeID, "visibility", "visible");
                            } else {
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
                                        'visibility': (hoverPosition === position) ? 'visible' : 'none'
                                    },
                                    'paint': {
                                        'line-color': '#' + position.colour,
                                        'line-width': 4
                                    }
                                });
                            }
                        }
                    };
                    request.send();
                }
            }
            hoverPosition = position;
        }
        
        setTimeout(function() {
            if (automaticRefresh) {
                updatePositionData();
            }
            setInterval(function() {
                if (automaticRefresh) {
                    updatePositionData();
                }
            }, 1000 * 60);
        }, 1000 * (timeToNextUpdate + 15));
    </script>

    % include('components/map_toggle')
% end
