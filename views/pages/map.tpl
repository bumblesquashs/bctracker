
% import json

% rebase('base')

<div id="page-header">
    <h1>Map</h1>
    % if visible_positions:
        <div class="options-container">
            <div class="option" onclick="toggleAutomaticRefresh()">
                <div id="auto-refresh-checkbox" class="checkbox {{ 'selected' if auto_refresh else '' }}">
                    % include('components/svg', name='check')
                </div>
                <span>Automatically Refresh</span>
            </div>
            <div class="option" onclick="toggleRouteLines()">
                <div id="show-route-lines-checkbox" class="checkbox {{ 'selected' if show_route_lines else '' }}">
                    % include('components/svg', name='check')
                </div>
                <span>Show Route Lines</span>
            </div>
            <div class="option" onclick="toggleNISBuses()">
                <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
                    % include('components/svg', name='check')
                </div>
                <span>Show NIS Buses</span>
            </div>
        </div>
    % end
</div>

% if visible_positions:
    <div id="map" class="full-screen"></div>
    
    % include('components/svg_script', name='fish')
    % include('components/svg_script', name='no-people')
    % include('components/svg_script', name='one-person')
    % include('components/svg_script', name='two-people')
    % include('components/svg_script', name='three-people')
    
    <script>
        const map = new ol.Map({
            target: 'map',
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM(),
                }),
            ],
            view: new ol.View({
                center: [0, 0],
                zoom: 1,
                maxZoom: 22
            }),
            interactions: ol.interaction.defaults.defaults().extend([
                new ol.interaction.DblClickDragZoom()
            ])
        });
        
        let positions = JSON.parse('{{! json.dumps([p.get_json() for p in positions]) }}');
        let currentShapeIDs = [];
        let markers = [];
        let routeLayers = {};
        let automaticRefresh = "{{ auto_refresh }}" !== "False";
        let showRouteLines = "{{ show_route_lines }}" !== "False";
        let showNISBuses = "{{ show_nis }}" !== "False";
        let hoverPosition = null;
        const busMarkerStyle = "{{ bus_marker_style }}";
        
        const shapes = {};
        
        document.body.onload = function() {
            map.updateSize();
        }
        
        updateMap(true);
        if (showRouteLines) {
            updateRouteData();
        }
        
        function updateMap(resetCoordinates) {
            currentShapeIDs = [];
            for (const marker of markers) {
                map.removeOverlay(marker);
            }
            markers = [];
            
            const area = new Area();
            
            for (const position of positions) {
                if (position.shape_id !== null && position.shape_id !== undefined) {
                    const shapeID = position.system_id + "_" + position.shape_id;
                    if (!(currentShapeIDs.includes(shapeID))) {
                        currentShapeIDs.push(shapeID);
                    }
                }
                
                const adherence = position.adherence;
                
                const element = document.createElement("div");
                element.id = "bus-marker-" + position.bus_number;
                element.className = "marker";
                if (position.shape_id === null || position.shape_id === undefined) {
                    element.classList.add("nis-bus");
                    if (!showNISBuses) {
                        element.classList.add("display-none");
                    }
                }
                if (position.bearing !== undefined) {
                    const sideWidthValue = busMarkerStyle == "mini" ? 8 : 16;
                    const bottomWidthValue = busMarkerStyle == "mini" ? 18 : 26;
                    const length = Math.floor(position.speed / 10);
                    const bearing = document.createElement("div");
                    bearing.className = "bearing";
                    if (busMarkerStyle === "adherence") {
                        bearing.classList.add('adherence');
                        if (adherence !== undefined && adherence !== null) {
                            bearing.classList.add(adherence.status_class)
                        }
                    } else if (busMarkerStyle === "occupancy") {
                        bearing.classList.add("occupancy");
                        bearing.classList.add(position.occupancy_status_class);
                    } else {
                        bearing.style.borderBottomColor = "#" + position.colour;
                    }
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
                if (adherence === null || adherence === undefined) {
                    headsign.className = "centred";
                    headsign.innerHTML = position.headsign;
                } else {
                    headsign.className = "row center gap-5";
                    const adherenceElement = document.createElement("div");
                    adherenceElement.classList.add("adherence-indicator", adherence.status_class);
                    adherenceElement.innerHTML = adherence.value;
                    
                    headsign.innerHTML = adherenceElement.outerHTML + position.headsign;
                }
                content.appendChild(headsign);
                
                const occupancy = document.createElement("div");
                occupancy.className = "row center gap-5";
                
                const occupancyIcon = document.createElement("div");
                occupancyIcon.className = "occupancy-icon";
                occupancyIcon.classList.add(position.occupancy_status_class);
                occupancyIcon.innerHTML = getSVG(position.occupancy_icon);
                occupancy.appendChild(occupancyIcon);
                
                const occupancyName = document.createElement("div");
                occupancyName.className = "occupancy-name";
                occupancyName.innerText = position.occupancy_name;
                occupancy.appendChild(occupancyName);
                
                content.appendChild(occupancy);
                
                if ("{{ system is None }}" === "True") {
                    const system = document.createElement("div");
                    system.className = "lighter-text centred";
                    system.innerHTML = position.system;
                    content.appendChild(system);
                }
                
                if (position.bus_number < 0) {
                    const icon = document.createElement("div");
                    icon.className = "icon";
                    if (busMarkerStyle == "route") {
                        icon.classList.add("bus_route");
                        icon.innerHTML = position.route_number;
                        icon.style.backgroundColor = "#" + position.colour;
                    } else if (busMarkerStyle == "mini") {
                        element.classList.add("small");
                        icon.classList.add("mini");
                        icon.style.backgroundColor = "#" + position.colour;
                    } else if (busMarkerStyle == "adherence") {
                        icon.classList.add("adherence");
                        if (adherence === undefined || adherence === null) {
                            icon.innerHTML = "N/A";
                        } else {
                            icon.innerHTML = adherence.value;
                            icon.classList.add(adherence.status_class);
                        }
                    } else if (busMarkerStyle == "occupancy") {
                        icon.classList.add("occupancy");
                        icon.classList.add(position.occupancy_status_class);
                        icon.innerHTML = getSVG(position.occupancy_icon);
                    } else {
                        icon.innerHTML = getSVG(position.bus_icon);
                        icon.style.backgroundColor = "#" + position.colour;
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
                    if (busMarkerStyle == "route") {
                        icon.classList.add("bus_route");
                        icon.innerHTML = "<div class='link'></div>" + position.route_number;
                        icon.style.backgroundColor = "#" + position.colour;
                    } else if (busMarkerStyle == "mini") {
                        element.classList.add("small");
                        icon.classList.add("mini");
                        icon.innerHTML = "<div class='link'></div>";
                        icon.style.backgroundColor = "#" + position.colour;
                    } else if (busMarkerStyle == "adherence") {
                        icon.classList.add("adherence");
                        if (adherence === undefined || adherence === null) {
                            icon.innerHTML = "<div class='link'></div>N/A";
                        } else {
                            icon.innerHTML = "<div class='link'></div>" + adherence.value;
                            icon.classList.add(adherence.status_class);
                        }
                    } else if (busMarkerStyle == "occupancy") {
                        icon.classList.add("occupancy");
                        icon.classList.add(position.occupancy_status_class);
                        icon.innerHTML = "<div class='link'></div>" + getSVG(position.occupancy_icon);
                    } else {
                        icon.innerHTML = "<div class='link'></div>" + getSVG(position.bus_icon);
                        icon.style.backgroundColor = "#" + position.colour;
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
                    area.combine(position.lat, position.lon);
                }
                
                const marker = new ol.Overlay({
                    position: ol.proj.fromLonLat([position.lon, position.lat]),
                    positioning: 'center-center',
                    element: element,
                    stopEvent: false,
                });
                map.addOverlay(marker);
                markers.push(marker);
            }
            
            if (resetCoordinates && area.isValid) {
                if (area.isPoint) {
                    map.getView().setCenter(ol.proj.fromLonLat(area.point));
                    map.getView().setZoom(15);
                } else {
                    map.getView().fit(ol.proj.transformExtent(area.box, ol.proj.get("EPSG:4326"), ol.proj.get("EPSG:3857")), {
                        padding: [100, 100, 100, 100]
                    });
                }
            }
            
            for (const shapeID in shapes) {
                if (currentShapeIDs.includes(shapeID)) {
                    shapes[shapeID].setVisible(showRouteLines);
                } else {
                    shapes[shapeID].setVisible(false);
                }
            }
        }
        
        function toggleAutomaticRefresh() {
            automaticRefresh = !automaticRefresh;
            const checkbox = document.getElementById("auto-refresh-checkbox");
            checkbox.classList.toggle("selected");
            setCookie("auto_refresh", automaticRefresh ? "true" : "false");
            
            if (automaticRefresh) {
                updatePositionData();
            }
        }
        
        function toggleRouteLines() {
            showRouteLines = !showRouteLines;
            const checkbox = document.getElementById("show-route-lines-checkbox");
            checkbox.classList.toggle("selected");
            setCookie("show_route_lines", showRouteLines ? "true" : "false");
            
            for (const shapeID of currentShapeIDs) {
                if (shapeID in shapes) {
                    shapes[shapeID].setVisible(showRouteLines);
                }
            }
            if (showRouteLines) {
                updateRouteData();
            }
        }
        
        function toggleNISBuses() {
            showNISBuses = !showNISBuses;
            const checkbox = document.getElementById("show-nis-checkbox");
            checkbox.classList.toggle("selected");
            setCookie("show_nis", showNISBuses ? "true" : "false");
            
            for (const element of document.getElementsByClassName("nis-bus")) {
                if (showNISBuses) {
                    element.classList.remove("display-none");
                } else {
                    element.classList.add("display-none");
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
                        if (showRouteLines) {
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
                if (shapeID in shapes) {
                    continue;
                }
                const request = new XMLHttpRequest();
                request.open("GET", getUrl(position.system_id, "api/shape/" + position.shape_id + ".json"), true);
                request.responseType = "json";
                request.onload = function() {
                    if (request.status === 200) {
                        if (shapeID in shapes) {
                            shapes[shapeID].setVisible(showRouteLines);
                        } else {
                            const layer = new ol.layer.Vector({
                                source: new ol.source.Vector({
                                    features: [
                                        new ol.Feature({
                                            geometry: new ol.geom.LineString(request.response.points.map(function (point) {
                                                return ol.proj.fromLonLat([point.lon, point.lat])
                                            })),
                                            name: shapeID
                                        })
                                    ],
                                    wrapX: false
                                }),
                                style: new ol.style.Style({
                                    stroke: new ol.style.Stroke({
                                        color: "#" + position.colour,
                                        width: 4,
                                        lineCap: "butt"
                                    })
                                }),
                                visible: showRouteLines
                            })
                            shapes[shapeID] = layer;
                            map.addLayer(layer);
                        }
                    }
                };
                request.send();
            }
        }
        
        function setHoverPosition(position) {
            if (showRouteLines) {
                return
            }
            if (hoverPosition !== null) {
                const shapeID = hoverPosition.system_id + "_" + hoverPosition.shape_id
                if (shapeID in shapes) {
                    shapes[shapeID].setVisible(false);
                }
            }
            if (position !== null) {
                if (position.shape_id === null || position.shape_id === undefined) {
                    return;
                }
                const shapeID = position.system_id + "_" + position.shape_id
                if (shapeID in shapes) {
                    shapes[shapeID].setVisible(true);
                } else {
                    const request = new XMLHttpRequest();
                    request.open("GET", getUrl(position.system_id, "api/shape/" + position.shape_id + ".json"), true);
                    request.responseType = "json";
                    request.onload = function() {
                        if (request.status === 200) {
                            if (shapeID in shapes) {
                                shapes[shapeID].setVisible(shapeID, hoverPosition == position);
                            } else {
                                const layer = new ol.layer.Vector({
                                    source: new ol.source.Vector({
                                        features: [
                                            new ol.Feature({
                                                geometry: new ol.geom.LineString(request.response.points.map(function (point) {
                                                    return ol.proj.fromLonLat([point.lon, point.lat])
                                                })),
                                                name: shapeID
                                            })
                                        ],
                                        wrapX: false
                                    }),
                                    style: new ol.style.Style({
                                        stroke: new ol.style.Stroke({
                                            color: "#" + position.colour,
                                            width: 4,
                                            lineCap: "butt"
                                        })
                                    }),
                                    visible: hoverPosition == position
                                })
                                shapes[shapeID] = layer;
                                map.addLayer(layer);
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
% else:
    <div class="container">
        <div class="section">
            <div class="options-container">
                <div class="option" onclick="toggleNISBusesEmpty()">
                    <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
                        % include('components/svg', name='check')
                    </div>
                    <div>Show NIS Buses</div>
                </div>
            </div>
            <script>
                function toggleNISBusesEmpty() {
                    window.location = "{{ get_url(system, 'map', show_nis='false' if show_nis else 'true') }}"
                }
            </script>
        </div>
        <div class="section">
            <div class="placeholder">
                % if not system:
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
                % elif not system.realtime_loaded:
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
% end
