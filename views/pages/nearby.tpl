
% rebase('base')

<div id="page-header">
    <h1>Nearby Stops</h1>
</div>

% include('components/svg_script', name='nearby')

<div class="page-container">
    <div id="current-location" class="sidebar container flex-1 display-none">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Current Location</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div id="map" class="preview"></div>
            </div>
        </div>
    </div>
    
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Upcoming Departures</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if context.system:
                    <div id="result" class="container">
                        <div id="nearby-status" class="loading column">
                            <div id="status-title">Loading upcoming departures...</div>
                            <div id="status-message" class="display-none"></div>
                        </div>
                    </div>
                % else:
                    <div class="placeholder">
                        <h3>Choose a system to see nearby stops</h3>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>System</th>
                                <th class="non-mobile align-right">Stops</th>
                                <th>Service Days</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for region in regions:
                                % region_systems = [s for s in systems if s.region == region]
                                % if region_systems:
                                    <tr class="header">
                                        <td colspan="3">{{ region }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % for system in sorted(region_systems):
                                        % count = len(system.get_stops())
                                        <tr>
                                            <td>
                                                <div class="row">
                                                    % include('components/agency_logo', agency=system.agency)
                                                    <div class="column">
                                                        <a href="{{ get_url(system, *path) }}">{{ system }}</a>
                                                        <span class="mobile-only smaller-font">
                                                            % if system.gtfs_loaded:
                                                                % if count == 1:
                                                                    1 Stop
                                                                % else:
                                                                    {{ count }} Stops
                                                                % end
                                                            % end
                                                        </span>
                                                    </div>
                                                </div>
                                            </td>
                                            % if system.gtfs_loaded:
                                                <td class="non-mobile align-right">{{ count }}</td>
                                                <td>
                                                    % include('components/weekdays', schedule=system.schedule, compact=True)
                                                </td>
                                            % else:
                                                <td class="lighter-text" colspan="2">Stops are loading...</td>
                                            % end
                                        </tr>
                                    % end
                                % end
                            % end
                        </tbody>
                    </table>
                % end
            </div>
        </div>
    </div>
</div>
            
<script>
    const map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM(),
                className: "ol-layer tile-layer"
            }),
        ],
        view: new ol.View({
            center: [0, 0],
            zoom: 1,
            maxZoom: 22
        }),
        interactions: [],
        controls: ol.control.defaults.defaults({
            zoom: false,
            rotate: false
        })
    });
    
    const systemSelected = "{{ context.system is not None }}" == "True";
    
    const statusElement = document.getElementById("nearby-status");
    const statusTitleElement = document.getElementById("status-title");
    const statusMessageElement = document.getElementById("status-message");
    
    let lat = null;
    let lon = null;
    
    function onSuccess(position) {
        lat = position.coords.latitude;
        lon = position.coords.longitude;
        
        const element = document.createElement("div");
        element.className = "marker";
        
        const icon = document.createElement("div");
        icon.className = "icon";
        icon.innerHTML = getSVG("nearby");
        
        element.appendChild(icon);
        
        map.addOverlay(new ol.Overlay({
            position: ol.proj.fromLonLat([lon, lat]),
            positioning: "center-center",
            element: element,
            stopEvent: false
        }));
        
        updateMap();
        
        if (systemSelected) {
            const request = new XMLHttpRequest();
            request.open("GET", "{{ get_url(context, 'frame', 'nearby') }}?lat=" + lat + "&lon=" + lon, true);
            request.onload = function() {
                if (request.status === 200) {
                    if (request.response === null) {
                        setStatus("error", "Error loading upcoming departures", "An unknown error occurred, please try again!");
                    } else {
                        setStatus("success", "Success", "Showing stops near " + lat + ", " + lon);
                        document.getElementById("result").innerHTML = request.response;
                    }
                } else {
                    setStatus("error", "Error loading upcoming departures", "An unknown error occurred, please try again!");
                }
            };
            request.onerror = function() {
                setStatus("error", "Error loading upcoming departures", "An unknown error occurred, please try again!");
            };
            request.send();
            
            loadMapMarkers(lat, lon);
        }
    }
    
    function loadMapMarkers(lat, lon) {
        const request = new XMLHttpRequest();
        request.open("GET", "{{ get_url(context, 'api', 'nearby.json') }}?lat=" + lat + "&lon=" + lon, true);
        request.responseType = "json";
        request.onload = function() {
            if (request.status === 200) {
                const stops = request.response.stops;
        
                for (const stop of stops) {
                    const element = document.createElement("div");
                    element.className = "marker small";
                    
                    const icon = document.createElement("a");
                    icon.className = "icon";
                    icon.href = getUrl(stop.system_id, "stops/" + stop.url_id, true);
                    icon.innerHTML = "<div class='link'></div>" + getSVG("stop");
                    
                    const details = document.createElement("div");
                    details.className = "details";
                    if (stop.number === null || stop.number === undefined) {
                        details.classList.add("hover-only");
                    }
                    
                    if (stop.number !== null && stop.number !== undefined) {
                        const title = document.createElement("div");
                        title.className = "title";
                        title.innerHTML = stop.number;
                        details.appendChild(title);
                    }
                    
                    const content = document.createElement("div");
                    content.classList = "content hover-only";
                    content.innerHTML = stop.name
                    
                    const routeList = document.createElement("div");
                    routeList.className = "route-list";
                    for (const route of stop.routes) {
                        routeList.innerHTML += "<span class='route' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
                    }
                    content.appendChild(routeList);
                    
                    details.appendChild(content);
                    
                    element.appendChild(icon);
                    element.appendChild(details);
                    
                    map.addOverlay(new ol.Overlay({
                        position: ol.proj.fromLonLat([stop.lon, stop.lat]),
                        positioning: "center-center",
                        element: element,
                        stopEvent: false
                    }));
                }
            }
        };
        request.send();
    }
    
    function onError(error) {
        const code = error.code;
        if (code == error.PERMISSION_DENIED) {
            setStatus("error", "Error loading upcoming departures", "Access to location is denied, give your browser access to your device's location to see nearby stops!");
        } else if (code == error.POSITION_UNAVAILABLE) {
            setStatus("error", "Error loading upcoming departures", "Location is unavailable, please try again!");
        } else if (code == error.TIMEOUT) {
            setStatus("error", "Error loading upcoming departures", "Timed out waiting for location, please try again!");
        } else {
            setStatus("error", "Error loading upcoming departures", "An unknown error occurred, please try again!");
        }
    }
    
    function setStatus(status, title, message = null) {
        statusElement.classList.remove("loading", "error", "success");
        statusElement.classList.add(status)
        
        statusTitleElement.innerHTML = title;
        if (message == null) {
            statusMessageElement.classList.add("display-none");
            statusMessageElement.innerHTML = "";
        } else {
            statusMessageElement.classList.remove("display-none");
            statusMessageElement.innerHTML = message;
        }
    }
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(onSuccess, onError);
    } else {
        setStatus("error", "Error loading upcoming departures", "Location is not supported, make sure you're using a device that has GPS");
    }
    
    document.body.onload = function() {
        map.updateSize();
        updateMap();
    }
    
    function updateMap() {
        if (lat !== null && lon !== null) {
            document.getElementById("current-location").classList.remove("display-none");
            map.updateSize();
            map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
            map.getView().setZoom(17);
        }
    }
</script>
