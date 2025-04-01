
% import json

% rebase('base')

% include('components/svg_script', name='fish')
% include('components/svg_script', name='no-people')
% include('components/svg_script', name='one-person')
% include('components/svg_script', name='two-people')
% include('components/svg_script', name='three-people')

<div id="page-header">
    <div class="row">
        <h1 class="flex-1">Map</h1>
        % if not system or system.realtime_enabled:
            % include('components/settings_toggle')
        % end
    </div>
</div>

<div id="no-buses-message" class="{{ 'display-none' if positions else '' }}">
    % if system and not system.realtime_enabled:
        <i>{{ system }} realtime information is not supported</i>
    % elif system:
        <i>There are no {{ system }} buses out right now</i>
    % else:
        <i>There are no buses out right now</i>
    % end
</div>

% if not system or system.realtime_enabled:
    <div id="settings" class="container collapsed">
        <div class="section">
            <div class="header">
                <h3>Options</h3>
            </div>
            <div class="content">
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
                    <div class="option" onclick="toggleStops()">
                        <div id="show-stops-checkbox" class="checkbox {{ 'selected' if show_stops else '' }}">
                            % include('components/svg', name='check')
                        </div>
                        <span>Show Stops</span>
                    </div>
                    <div class="option" onclick="toggleNISBuses()">
                        <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
                            % include('components/svg', name='check')
                        </div>
                        <span>Show NIS Buses</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h3>Icon Style</h3>
            </div>
            <div class="content">
                <div class="options-container">
                    <div class="option" onclick="setBusMarkerStyle('default')">
                        <div id="bus-marker-style-default" class="radio-button {{ 'selected' if not bus_marker_style or bus_marker_style == 'default' else '' }}"></div>
                        <div>Bus Type</div>
                    </div>
                    <div class="option" onclick="setBusMarkerStyle('mini')">
                        <div id="bus-marker-style-mini" class="radio-button {{ 'selected' if bus_marker_style == 'mini' else '' }}"></div>
                        <div>Mini</div>
                    </div>
                    <div class="option" onclick="setBusMarkerStyle('route')">
                        <div id="bus-marker-style-route" class="radio-button {{ 'selected' if bus_marker_style == 'route' else '' }}"></div>
                        <div>Route Number</div>
                    </div>
                    <div class="option" onclick="setBusMarkerStyle('adherence')">
                        <div id="bus-marker-style-adherence" class="radio-button {{ 'selected' if bus_marker_style == 'adherence' else '' }}"></div>
                        <div>Schedule Adherence</div>
                    </div>
                    <div class="option" onclick="setBusMarkerStyle('occupancy')">
                        <div id="bus-marker-style-occupancy" class="radio-button {{ 'selected' if bus_marker_style == 'occupancy' else '' }}"></div>
                        <div>Occupancy</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
% end

% if stop_area:
    <script>
        const initialArea = new Area("{{ stop_area.min_lat }}", "{{ stop_area.max_lat }}", "{{ stop_area.min_lon }}", "{{ stop_area.max_lon }}");
        const initialTopPadding = window.screen.width > 1000 ? 100 : 200;
        const initialLeftPadding = window.screen.width > 1000 ? 400 : 100;
        map.getView().fit(ol.proj.transformExtent(initialArea.box, ol.proj.get("EPSG:4326"), ol.proj.get("EPSG:3857")), {
            padding: [initialTopPadding, 100, 100, initialLeftPadding]
        });
    </script>
% end

<script>
    let positions = JSON.parse('{{! json.dumps([p.get_json() for p in positions]) }}');
    let currentShapeIDs = [];
    let routeLayers = {};
    let automaticRefresh = "{{ auto_refresh }}" !== "False";
    let showRouteLines = "{{ show_route_lines }}" !== "False";
    let showStops = "{{ show_stops }}" !== "False";
    let showNISBuses = "{{ show_nis }}" !== "False";
    let busMarkerStyle = "{{ bus_marker_style or 'default' }}";
    let hoverPosition = null;
    
    let busMarkers = [];
    
    const shapes = {};
    
    const cachedStops = {};
    const stopMarkers = {};
    let currentStopKeys = new Set();
    
    document.body.onload = function() {
        map.updateSize();
    }
    
    updateMap(true);
    if (showRouteLines) {
        updateRouteData();
    }
    
    map.on('moveend', function(event) {
        const zoom = map.getView().getZoom();
        const extent = map.getView().calculateExtent(map.getSize());
        const box = ol.proj.transformExtent(extent, 'EPSG:3857', 'EPSG:4326');
        updateStops(zoom, box);
    });
    
    function updateMap(resetCoordinates) {
        currentShapeIDs = [];
        for (const marker of busMarkers) {
            map.removeOverlay(marker);
        }
        busMarkers = [];
        
        const area = new Area();
        
        if (positions.length === 0) {
            document.getElementById("no-buses-message").classList.remove("display-none");
        } else {
            document.getElementById("no-buses-message").classList.add("display-none");
        }
        
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
            
            let icon;
            if (position.bus_number < 0) {
                icon = document.createElement("div");
            } else {
                icon = document.createElement("a");
                if (currentSystemID === null) {
                    icon.href = getUrl(currentSystemID, "bus/" + position.agency_id + "/" + position.bus_url_id, true);
                } else {
                    icon.href = getUrl(currentSystemID, "bus/" + position.bus_url_id, true);
                }
                icon.innerHTML = "<div class='link'></div>"
            }
            icon.className = "icon";
            icon.onmouseenter = function() {
                setHoverPosition(position);
            }
            icon.onmouseleave = function() {
                setHoverPosition(null);
            }
            element.appendChild(icon);
            
            if (busMarkerStyle === "route") {
                icon.classList.add("bus_route");
                if (position.lat === 0 && position.lon === 0) {
                    icon.innerHTML += getSVG("fish");
                } else {
                    icon.innerHTML += position.route_number;
                }
                icon.style.backgroundColor = "#" + position.colour;
            } else if (busMarkerStyle === "mini") {
                element.classList.add("small");
                icon.classList.add("mini");
                icon.style.backgroundColor = "#" + position.colour;
            } else if (busMarkerStyle === "adherence") {
                icon.classList.add("adherence");
                if (adherence === undefined || adherence === null) {
                    if (position.lat === 0 && position.lon === 0) {
                        icon.innerHTML += getSVG("fish");
                    } else if (position.route_number === "NIS") {
                        icon.innerHTML += "NIS";
                    } else {
                        icon.innerHTML += "N/A"
                    }
                } else {
                    if (position.lat === 0 && position.lon === 0) {
                        icon.innerHTML += getSVG("fish");
                    } else {
                        icon.innerHTML += adherence.value;
                    }
                    icon.classList.add(adherence.status_class);
                    const adherenceValue = parseInt(adherence.value);
                    if (adherenceValue >= 100 || adherenceValue <= -100) {
                        icon.classList.add("smaller-font");
                    }
                }
            } else if (busMarkerStyle === "occupancy") {
                icon.classList.add("occupancy");
                icon.classList.add(position.occupancy_status_class);
                if (position.lat === 0 && position.lon === 0) {
                    icon.innerHTML += getSVG("fish");
                } else {
                    icon.innerHTML += getSVG(position.occupancy_icon);
                }
            } else {
                if (position.lat === 0 && position.lon === 0) {
                    icon.innerHTML += getSVG("fish");
                } else {
                    icon.innerHTML += getSVG(position.bus_icon);
                }
                icon.style.backgroundColor = "#" + position.colour;
            }
            
            const details = document.createElement("div");
            details.className = "details";
            element.appendChild(details);
            
            const title = document.createElement("div");
            title.className = "title";
            title.innerHTML = position.bus_display;
            if (position.adornment != null) {
                title.innerHTML += " <span class='adornment'>" + position.adornment + "</span>";
            }
            details.appendChild(title);
            
            const content = document.createElement("div");
            content.className = "content hover-only";
            details.appendChild(content);
            
            const model = document.createElement("div");
            model.className = "lighter-text";
            model.innerHTML = position.bus_order;
            content.appendChild(model);
            
            const headsign = document.createElement("div");
            if (position.headsign === "Not In Service") {
                headsign.innerHTML = position.headsign;
            } else {
                headsign.className = "headsign";
            
                const routeLine = document.createElement("div");
                routeLine.className = "route-line";
                routeLine.style.backgroundColor = "#" + position.colour;
                
                headsign.innerHTML = routeLine.outerHTML + position.headsign;
            }
            content.appendChild(headsign);
        
            const footer = document.createElement("div");
            footer.className = "lighter-text";
            content.appendChild(footer);
            
            const systemElement = document.createElement("span");
            systemElement.innerHTML = position.system;
            footer.appendChild(systemElement);
            
            if (position.timestamp) {
                if (systemElement) {
                    const separator = document.createElement("span")
                    separator.innerHTML = " • ";
                    footer.appendChild(separator);
                }
                const timestamp = document.createElement("span");
                footer.appendChild(timestamp);
                updateTimestampFunctions.push(function(currentTime) {
                    const difference = getDifference(currentTime, (position.timestamp * 1000) + timestampOffset);
                    timestamp.innerHTML = difference;
                });
            }
            
            const iconsRow = document.createElement("div");
            iconsRow.className = "row center gap-5";
            content.appendChild(iconsRow);
            
            if (adherence !== null && adherence !== undefined) {
                const adherenceElement = document.createElement("div");
                adherenceElement.classList.add("adherence-indicator", adherence.status_class);
                adherenceElement.innerHTML = adherence.value;
                iconsRow.appendChild(adherenceElement);
            }
            
            const occupancyIcon = document.createElement("div");
            occupancyIcon.className = "occupancy-icon";
            occupancyIcon.classList.add(position.occupancy_status_class);
            occupancyIcon.innerHTML = getSVG(position.occupancy_icon);
            iconsRow.appendChild(occupancyIcon);
            
            const agencyLogo = document.createElement("img");
            agencyLogo.className = "agency-logo";
            agencyLogo.src = "/img/icons/" + position.agency_id + ".png";
            agencyLogo.onerror = function() {
                agencyLogo.style.visibility = 'hidden';
            };
            iconsRow.appendChild(agencyLogo);
            
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
            busMarkers.push(marker);
        }
        
        if (resetCoordinates && area.isValid) {
            if (area.isPoint) {
                map.getView().setCenter(ol.proj.fromLonLat(area.point));
                map.getView().setZoom(15);
            } else {
                const topPadding = window.screen.width > 1000 ? 100 : 200;
                const leftPadding = window.screen.width > 1000 ? 400 : 100;
                map.getView().fit(ol.proj.transformExtent(area.box, ol.proj.get("EPSG:4326"), ol.proj.get("EPSG:3857")), {
                    padding: [topPadding, 100, 100, leftPadding]
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
    
    function toggleStops() {
        showStops = !showStops;
        const checkbox = document.getElementById("show-stops-checkbox");
        checkbox.classList.toggle("selected");
        setCookie("show_stops", showStops ? "true" : "false");
        
        if (showStops) {
            const zoom = map.getView().getZoom();
            const extent = map.getView().calculateExtent(map.getSize());
            const box = ol.proj.transformExtent(extent, 'EPSG:3857', 'EPSG:4326');
            updateStops(zoom, box);
        } else {
            for (key in stopMarkers) {
                removeStopMarkers(key);
            }
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
    
    function setBusMarkerStyle(style) {
        document.getElementById("bus-marker-style-" + busMarkerStyle).classList.remove("selected");
        busMarkerStyle = style;
        document.getElementById("bus-marker-style-" + style).classList.add("selected");
        setCookie("bus_marker_style", style);
        updateMap(false);
    }
    
    function updatePositionData() {
        const request = new XMLHttpRequest();
        request.open("GET", "{{ get_url(system, 'api', 'positions') }}", true);
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
            request.open("GET", getUrl(position.system_id, "api/shape/" + position.shape_id), true);
            request.responseType = "json";
            request.onload = function() {
                if (request.status === 200) {
                    if (shapeID in shapes) {
                        shapes[shapeID].setVisible(showRouteLines);
                    } else {
                        const layer = new ol.layer.Vector({
                            className: "ol-layer route-layer",
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
                            visible: showRouteLines,
                            zIndex: 1
                        });
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
                request.open("GET", getUrl(position.system_id, "api/shape/" + position.shape_id), true);
                request.responseType = "json";
                request.onload = function() {
                    if (request.status === 200) {
                        if (shapeID in shapes) {
                            shapes[shapeID].setVisible(shapeID, hoverPosition == position);
                        } else {
                            const layer = new ol.layer.Vector({
                                className: "ol-layer route-layer",
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
                                visible: hoverPosition == position,
                                zIndex: 1
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
    
    function updateStops(zoom, box) {
        if (!showStops) {
            return
        }
        const minZoom = window.screen.width > 1000 ? 14.5 : 14;
        if (zoom >= minZoom) {
            const minLat = box[1];
            const maxLat = box[3];
            const latPadding = (maxLat - minLat) / 2;
            
            const minLon = box[0];
            const maxLon = box[2];
            const lonPadding = (maxLon - minLon) / 2;
            
            const size = 0.01;
            
            const firstLat = Math.round((minLat - latPadding - size) * 100) / 100;
            const firstLon = Math.round((minLon - lonPadding - size) * 100) / 100;
            const lastLat = Math.round((maxLat + latPadding + size) * 100) / 100;
            const lastLon = Math.round((maxLon + lonPadding + size) * 100) / 100;
            
            let newStopKeys = new Set();
            for (let lat = firstLat; lat <= lastLat; lat += size) {
                for (let lon = firstLon; lon <= lastLon; lon += size) {
                    const roundedLat = Math.round(lat * 100) / 100;
                    const roundedLon = Math.round(lon * 100) / 100;
                    const key = roundedLat + ":" + roundedLon;
                    newStopKeys.add(key);
                    loadStops(key, roundedLat, roundedLon, size);
                }
            }
            for (const key of currentStopKeys.difference(newStopKeys)) {
                removeStopMarkers(key);
            }
            currentStopKeys = newStopKeys;
        } else {
            for (const key in stopMarkers) {
                removeStopMarkers(key);
            }
        }
    }
    
    function removeStopMarkers(key) {
        if (key in stopMarkers) {
            for (const marker of stopMarkers[key]) {
                map.removeOverlay(marker);
            }
            stopMarkers[key] = [];
        }
    }
    
    function loadStops(key, lat, lon, size) {
        if (key in cachedStops) {
            updateStopMarkers(key);
        } else {
            const url = getUrl(currentSystemID, "api/stops", false, {
                "lat": lat,
                "lon": lon,
                "size": size
            });
            const request = new XMLHttpRequest();
            request.open("GET", url, true);
            request.responseType = "json";
            request.onload = function() {
                if (request.status === 200) {
                    cachedStops[key] = request.response.stops;
                    updateStopMarkers(key);
                }
            };
            request.send();
        }
    }
    
    function updateStopMarkers(key) {
        if (key in stopMarkers && stopMarkers[key].length > 0) {
            return
        }
        let markers = [];
        for (const stop of cachedStops[key]) {
            const element = document.createElement("div");
            element.className = "marker small";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = getUrl(stop.system_id, "stops/" + stop.url_id, true);
            icon.innerHTML = "<div class='link'></div>" + getSVG("stop");
            if (stop.routes.length > 0) {
                icon.style.backgroundColor = "#" + stop.routes[0].colour;
            } else {
                icon.style.backgroundColor = "#666666";
            }
            
            const details = document.createElement("div");
            details.className = "details hover-only";
            
            if (stop.number !== null && stop.number !== undefined) {
                const title = document.createElement("div");
                title.className = "title";
                title.innerHTML = stop.number;
                details.appendChild(title);
            }
            
            const content = document.createElement("div");
            content.className = "content";
            content.innerHTML = stop.name
            
            const routeList = document.createElement("div");
            routeList.className = "route-list";
            for (const route of stop.routes) {
                routeList.innerHTML += "<span class='route' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
            }
            content.appendChild(routeList);
            
            const agencyLogo = document.createElement("img");
            agencyLogo.className = "agency-logo";
            agencyLogo.src = "/img/icons/" + stop.agency_id + ".png";
            agencyLogo.onerror = function() {
                agencyLogo.style.visibility = 'hidden';
            };
            content.innerHTML += "<div class='row gap-5'>" + agencyLogo.outerHTML + stop.system_name + "</div>";
            
            details.appendChild(content);
            
            element.appendChild(icon);
            element.appendChild(details);
            
            const marker = new ol.Overlay({
                position: ol.proj.fromLonLat([stop.lon, stop.lat]),
                positioning: "center-center",
                element: element,
                stopEvent: false
            })
            map.addOverlay(marker);
            markers.push(marker);
        }
        stopMarkers[key] = markers;
    }
</script>

% if not system or system.realtime_enabled:
    <script>
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
% end
