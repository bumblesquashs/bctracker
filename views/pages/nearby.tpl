
% rebase('base')

<div id="page-header">
    <h1>Nearby Stops</h1>
</div>

% include('components/svg_script', name='location')

<div class="page-container">
    <div id="current-location" class="sidebar container flex-1 display-none">
        <div class="section">
            <div class="header">
                <h2>Current Location</h2>
            </div>
            <div class="content">
                <div id="map" class="preview"></div>
            </div>
        </div>
    </div>
    
    <div class="container flex-3">
        <div class="section">
            <div class="header">
                <h2>Upcoming Departures</h2>
            </div>
            <div class="content">
                % if system is None:
                    <div class="placeholder">
                        <h3>Choose a system to see nearby stops</h3>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>System</th>
                                <th class="non-mobile"># Stops</th>
                                <th>Service Days</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for region in regions:
                                % region_systems = [s for s in systems if s.region == region]
                                % if len(region_systems) > 0:
                                    <tr class="header">
                                        <td colspan="3">{{ region }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % for region_system in sorted(region_systems):
                                        % count = len(region_system.get_stops())
                                        <tr>
                                            <td>
                                                <div class="column">
                                                    <a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
                                                    <span class="mobile-only smaller-font">
                                                        % if region_system.gtfs_loaded:
                                                            % if count == 1:
                                                                1 Stop
                                                            % else:
                                                                {{ count }} Stops
                                                            % end
                                                        % end
                                                    </span>
                                                </div>
                                            </td>
                                            % if region_system.gtfs_loaded:
                                                <td class="non-mobile">{{ count }}</td>
                                                <td>
                                                    % include('components/weekdays', schedule=region_system.schedule, compact=True)
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
                % else:
                    <div id="result" class="container">
                        <div id="nearby-status" class="loading column">
                            <div id="status-title">Loading upcoming departures...</div>
                            <div id="status-message" class="display-none"></div>
                        </div>
                    </div>
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
                source: new ol.source.OSM()
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
    
    const systemSelected = "{{ system is not None }}" == "True";
    
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
        icon.innerHTML = getSVG("location");
        
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
            request.open("GET", "{{get_url(system, 'frame/nearby')}}?lat=" + lat + "&lon=" + lon, true);
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
        request.open("GET", "{{get_url(system, 'api/nearby.json')}}?lat=" + lat + "&lon=" + lon, true);
        request.responseType = "json";
        request.onload = function() {
            if (request.status === 200) {
                const stops = request.response.stops;
        
                for (const stop of stops) {
                    const element = document.createElement("div");
                    element.className = "marker small";
                    
                    const icon = document.createElement("a");
                    icon.className = "icon";
                    icon.href = getUrl(stop.system_id, "stops/" + stop.number);
                    icon.innerHTML = "<div class='link'></div>" + getSVG("stop");
                    
                    const details = document.createElement("div");
                    details.className = "details";
                    
                    const title = document.createElement("div");
                    title.className = "title";
                    title.innerHTML = stop.number;
                    
                    const content = document.createElement("div");
                    content.classList = "content hover-only centred";
                    let routesHTML = "";
                    for (const route of stop.routes) {
                        routesHTML += "<span class='route' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
                    }
                    content.innerHTML = stop.name + "<div>" + routesHTML + "</div>";
                    
                    details.appendChild(title);
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
            setStatus("error", "Error loading upcoming departures", "Access to location is denied, give your browser access to your devices's location to see nearby stops!");
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
            map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
            map.getView().setZoom(17);
        }
    }
</script>
