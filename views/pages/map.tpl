
% import json

% rebase('base')

<div class="page-header">
    <h1 class="title">Map</h1>
    % if len(visible_positions) > 0:
        <div class="flex-column flex-gap-5">
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
                    <div id="nis-image" class="{{ '' if show_nis else 'hidden' }}">
                        <img class="white" src="/img/white/check.png" />
                        <img class="black" src="/img/black/check.png" />
                    </div>
                </div>
                <span class="checkbox-label">Show NIS Buses</span>
            </div>
        </div>
    % end
</div>

% if len(visible_positions) == 0:
    <div class="container">
        <div class="section">
            <div class="checkbox" onclick="toggleNISBusesEmpty()">
                <div class="box">
                    <div id="nis-image" class="{{ '' if show_nis else 'hidden' }}">
                        <img class="white" src="/img/white/check.png" />
                        <img class="black" src="/img/black/check.png" />
                    </div>
                </div>
                <span class="checkbox-label">Show NIS Buses</span>
            </div>
            <script>
                function toggleNISBusesEmpty() {
                    window.location = "{{ get_url(system, 'map', show_nis='false' if show_nis else 'true') }}"
                }
            </script>
        </div>
        <div class="section">
            <div class="placeholder">
                % if system is None:
                    % if show_nis:
                        <h3>There are no buses out right now</h3>
                        <p>
                            BC Transit does not have late night service, so this should be the case overnight.
                            If you look out your window and the sun is shining, there may be an issue getting up-to-date info.
                        </p>
                        <p>Please check again later!</p>
                    % else:
                        <h3>There are no buses in service right now</h3>
                        <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
                    % end
                % elif not system.realtime_enabled:
                    <h3>{{ system }} does not support realtime</h3>
                    <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
                    <div class="non-desktop">
                        % include('components/systems')
                    </div>
                % elif not system.is_loaded:
                    <h3>Realtime information for {{ system }} is unavailable</h3>
                    <p>System data is currently loading and will be available soon.</p>
                % elif not show_nis:
                    <h3>There are no buses in service in {{ system }} right now</h3>
                    <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
                % else:
                    <h3>There are no buses out in {{ system }} right now</h3>
                    <p>Please check again later!</p>
                % end
            </div>
        </div>
    </div>
% else:
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
        
        let positions = JSON.parse('{{! json.dumps([p.get_json() for p in positions]) }}');
        let currentShapeIDs = [];
        let markers = [];
        let tripLinesVisible = false;
        let automaticRefresh = false;
        let showNISBuses = "{{ show_nis }}" !== "False";
        let hoverPosition = null;
        const busMarkerStyle = "{{ bus_marker_style }}";
        
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
                    headsign.className = "flex-row center flex-gap-5";
                    const adherence = position.adherence;
                    const adherenceElement = document.createElement("div");
                    adherenceElement.classList.add("adherence-indicator");
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
                    
                    icon.onmouseenter = function() {
                        setHoverPosition(position);
                    }
                    icon.onmouseleave = function() {
                        setHoverPosition(null);
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
                    
                    icon.onmouseenter = function() {
                        setHoverPosition(position);
                    }
                    icon.onmouseleave = function() {
                        setHoverPosition(null);
                    }
                    element.appendChild(icon);
                }
                
                if (position.adornment != null) {
                    title.innerHTML += " <span class='adornment'>" + position.adornment + "</span>";
                }
                
                details.appendChild(title);
                details.appendChild(content);
                element.appendChild(details);
                
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
            setCookie("show_nis", showNISBuses ? "true" : "false");
            
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
