
% rebase('base')

<div class="page-header">
    <h1 class="title">Nearby Stops</h1>
</div>

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div id="current-location" class="section display-none">
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
                        <h3 class="title">Choose a system to see nearby stops</h3>
                    </div>
                    <div class="non-desktop">
                        % include('components/systems')
                    </div>
                % else:
                    <div id="result" class="container">
                        <div id="nearby-status" class="loading flex-column">
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
    const map = new mapboxgl.Map({
        container: "map",
        center: [0, 0],
        zoom: 1,
        style: mapStyle,
        interactive: false
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
        icon.innerHTML = "<img src='/img/white/location.png' />";
        
        element.appendChild(icon);
        
        new mapboxgl.Marker(element).setLngLat([lon, lat]).addTo(map);
        
        updateMap();
        
        if (systemSelected) {
            const request = new XMLHttpRequest();
            request.open("GET", "{{get_url(system, 'frame/nearby')}}?lat=" + lat + "&lon=" + lon, true);
            request.onload = function() {
                if (request.status === 200) {
                    if (request.response === null) {
                        setStatus("error", "Error loading upcoming departures", "An unknown error occurred");
                    } else {
                        setStatus("success", "Success", "Showing stops near " + lat + ", " + lon);
                        document.getElementById("result").innerHTML = request.response;
                    }
                } else {
                    setStatus("error", "Error loading upcoming departures", "An unknown error occurred");
                }
            };
            request.onerror = function() {
                setStatus("error", "Error loading upcoming departures", "An unknown error occurred");
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
                    icon.innerHTML = "<div class='link'></div><img src='/img/white/stop.png' />";
                    
                    const details = document.createElement("div");
                    details.className = "details";
                    
                    const title = document.createElement("div");
                    title.className = "title";
                    title.innerHTML = stop.number;
                    
                    const content = document.createElement("div");
                    content.classList = "content hover-only centred";
                    let routesHTML = "";
                    for (const route of stop.routes) {
                        routesHTML += "<span class='route-number' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
                    }
                    content.innerHTML = stop.name + "<div>" + routesHTML + "</div>";
                    
                    details.appendChild(title);
                    details.appendChild(content);
                    
                    element.appendChild(icon);
                    element.appendChild(details);
                    
                    new mapboxgl.Marker(element).setLngLat([stop.lon, stop.lat]).addTo(map);
                }
            }
        };
        request.send();
    }
    
    function onError(error) {
        const code = error.code;
        if (code == error.PERMISSION_DENIED) {
            setStatus("error", "Error loading upcoming departures", "Access to location is denied");
        } else if (code == error.POSITION_UNAVAILABLE) {
            setStatus("error", "Error loading upcoming departures", "Location is unavailable");
        } else if (code == error.TIMEOUT) {
            setStatus("error", "Error loading upcoming departures", "Timed out waiting for location");
        } else {
            setStatus("error", "Error loading upcoming departures", "An unknown error occurred");
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
        setStatus("error", "Error loading upcoming departures", "Location is not supported");
    }
    
    map.on("load", function() {
        map.resize();
        updateMap();
    });
    
    function updateMap() {
        if (lat !== null && lon !== null) {
            document.getElementById("current-location").classList.remove("display-none");
            map.jumpTo({
                center: [lon, lat],
                zoom: 16
            });
        }
    }
</script>
