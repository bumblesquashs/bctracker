
% rebase('base')

<div class="page-header">
    <h1 class="title">Nearby</h1>
</div>

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <h2>Current Location</h2>
            <div id="map" class="preview"></div>
        </div>
        
        <div class="section">
            <div id="nearby-status" class="loading flex-column">
                <div id="status-title" class="">Loading nearby buses, routes, and stops...</div>
                <div id="status-message" style="display: none;"></div>
            </div>
        </div>
    </div>
    <div id="result" class="container flex-3">
        
    </div>
</div>

<style>
    #nearby-status {
        padding: 10px;
        border-radius: 10px;
    }
    
    #nearby-status.loading {
        border: 2px solid #0000FF;
        background-color: #CCCCFF;
    }
    
    #nearby-status.error {
        border: 2px solid #FF0000;
        background-color: #FFCCCC;
    }
    
    #nearby-status.success {
        display: none;
    }
</style>

<script>
    const map = new mapboxgl.Map({
        container: "map",
        center: [0, 0],
        zoom: 1,
        style: mapStyle,
        interactive: false
    });
    
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
        const request = new XMLHttpRequest();
        request.open("GET", "{{get_url(system, 'frame/nearby')}}?lat=" + lat + "&lon=" + lon, true);
        request.onload = function() {
            if (request.status === 200) {
                if (request.response === null) {
                    setStatus("error", "Error", "Unable to load nearby transit");
                } else {
                    setStatus("success", "Success", "Showing transit near " + lat + ", " + lon);
                    document.getElementById("result").innerHTML = request.response;
                }
            } else {
                setStatus("error", "Error", "Unable to load nearby transit");
            }
        };
        request.onerror = function() {
            setStatus("error", "Error", "Unable to load nearby transit");
        };
        request.send();
    }
    
    function onError(error) {
        const code = error.code;
        if (code == error.PERMISSION_DENIED) {
            setStatus("error", "Error", "Access to location is denied");
        } else if (code == error.POSITION_UNAVAILABLE) {
            setStatus("error", "Error", "Location is unavailable");
        } else if (code == error.TIMEOUT) {
            setStatus("error", "Error", "Timed out waiting for location");
        } else {
            setStatus("error", "Error", "An unknown error occurred");
        }
    }
    
    function setStatus(status, title, message = null) {
        statusElement.classList.remove("loading", "error", "success");
        statusElement.classList.add(status)
        
        statusTitleElement.innerHTML = title;
        if (message == null) {
            statusMessageElement.style.display = "none";
            statusMessageElement.innerHTML = "";
        } else {
            statusMessageElement.style.display = "block";
            statusMessageElement.innerHTML = message;
        }
    }
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(onSuccess, onError);
    } else {
        loadingElement.style.display = "none";
        errorElement.style.display = "block";
        errorMessageElement.innerHTML = "Location is not supported";
    }
    
    map.on("load", function() {
        map.resize();
        updateMap();
    });
    
    function updateMap() {
        if (lat === null || lon === null) {
            document.getElementById("map").style.display = "none";
        } else {
            map.jumpTo({
                center: [lon, lat],
                zoom: 14
            });
        }
    }
</script>
