<div id="map-controls">
    <div id="zoom-in-control" class="control" onclick="zoomIn()">
        % include('components/svg', name='plus')
    </div>
    <div id="zoom-out-control" class="control" onclick="zoomOut()">
        % include('components/svg', name='minus')
    </div>
    <div id="rotation-control" class="control disabled">
        <div id="rotation-control-arrow">
            % include('components/svg', name='navigation')
        </div>
    </div>
    <div id="geolocation-control" class="control" onclick="toggleGeolocation()">
        <div id="geolocation-tracking-icon">
            % include('components/svg', name='geolocation-tracking')
        </div>
        <div id="geolocation-enabled-icon" class="display-none">
            % include('components/svg', name='geolocation-enabled')
        </div>
    </div>
    <div class="control mobile-only" onclick="toggleFullscreen()">
        <div id="open-fullscreen-icon">
            % include('components/svg', name='fullscreen-open')
        </div>
        <div id="close-fullscreen-icon" class="display-none">
            % include('components/svg', name='fullscreen-close')
        </div>
    </div>
</div>

<script>
    let geolocationEnabled = false;
    let geolocationError = null;
    let followGeolocation = false;
    let setFollowZoom = false;
        
    const geolocation = new ol.Geolocation({
        trackingOptions: {
          enableHighAccuracy: true
        },
        projection: map.getView().getProjection()
    });
    
    geolocation.on('error', function (error) {
        geolocationError = error;
        const control = document.getElementById("geolocation-control");
        const trackingIcon = document.getElementById("geolocation-tracking-icon");
        const enabledIcon = document.getElementById("geolocation-enabled-icon");
        
        control.onclick = null;
        control.classList.remove("active");
        control.classList.add("disabled", "error");
        trackingIcon.classList.remove("display-none");
        enabledIcon.classList.add("display-none");
    });
    
    const accuracyFeature = new ol.Feature();
    geolocation.on('change:accuracyGeometry', function () {
        accuracyFeature.setGeometry(geolocation.getAccuracyGeometry());
    });
    
    const positionFeature = new ol.Feature();
    positionFeature.setStyle(
        new ol.style.Style({
            image: new ol.style.Circle({
                radius: 6,
                fill: new ol.style.Fill({
                    color: "#3399CC"
                }),
                stroke: new ol.style.Stroke({
                    color: "#FFFFFF",
                    width: 2
                })
            })
        })
    );
    geolocation.on('change:position', function () {
        const coordinates = geolocation.getPosition();
        if (coordinates) {
            positionFeature.setGeometry(new ol.geom.Point(coordinates));
            if (followGeolocation) {
                if (setFollowZoom) {
                    setFollowZoom = false;
                    map.getView().animate({
                        center: coordinates,
                        zoom: 15,
                        duration: 500
                    });
                } else {
                    map.getView().animate({
                        center: coordinates,
                        duration: 50
                    });
                }
            }
        }
    });
    
    new ol.layer.Vector({
        map: map,
        source: new ol.source.Vector({
            features: [accuracyFeature, positionFeature]
        }),
        zIndex: 10
    });
    
    map.on('moveend', function(event) {
        const zoom = map.getView().getZoom();
        const zoomInControl = document.getElementById("zoom-in-control");
        const zoomOutControl = document.getElementById("zoom-out-control");
        
        if (zoom === 22) {
            zoomInControl.classList.add("disabled");
            zoomInControl.onclick = null;
        } else {
            zoomInControl.classList.remove("disabled");
            zoomInControl.onclick = zoomIn;
        }
        if (zoom === 3) {
            zoomOutControl.classList.add("disabled");
            zoomOutControl.onclick = null;
        } else {
            zoomOutControl.classList.remove("disabled");
            zoomOutControl.onclick = zoomOut;
        }
    });
    
    map.on('pointermove', function(event) {
        if (geolocationError !== null) {
            return
        }
        if (event.dragging && followGeolocation) {
            followGeolocation = false;
            setFollowZoom = false;
            updateGeolocationControl();
        }
    })
    
    map.getView().on('change:rotation', function(event) {
        const rotation = map.getView().getRotation();
        const rotationControl = document.getElementById("rotation-control");
        const rotationControlArrow = document.getElementById("rotation-control-arrow");
        
        if (rotation === 0) {
            rotationControl.classList.add("disabled");
            rotationControl.onclick = null;
        } else {
            rotationControl.classList.remove("disabled");
            rotationControl.onclick = resetRotation;
        }
        rotationControlArrow.style.transform = "rotate(" + rotation + "rad)";
    })
    
    function zoomIn() {
        map.getView().animate({
            zoom: Math.min(map.getView().getZoom() + 1, 22),
            duration: 250
        });
    }
    
    function zoomOut() {
        map.getView().animate({
            zoom: Math.max(map.getView().getZoom() - 1, 3),
            duration: 250
        });
    }
    
    function resetRotation() {
        map.getView().animate({
            rotation: 0,
            duration: 250
        });
    }
    
    function toggleGeolocation() {
        if (geolocationEnabled) {
            if (followGeolocation) {
                geolocationEnabled = false;
                followGeolocation = false;
                setFollowZoom = false;
                geolocation.setTracking(false);
                accuracyFeature.setGeometry(null);
                positionFeature.setGeometry(null);
            } else {
                followGeolocation = true;
                setFollowZoom = false;
                const coordinates = geolocation.getPosition();
                if (coordinates) {
                    map.getView().animate({
                        center: coordinates,
                        zoom: 15,
                        duration: 500
                    });
                }
            }
        } else {
            geolocationEnabled = true;
            followGeolocation = true;
            setFollowZoom = true;
            geolocation.setTracking(true);
        }
        updateGeolocationControl();
    }
    
    function toggleFullscreen() {
        document.getElementById("open-fullscreen-icon").classList.toggle('display-none');
        document.getElementById("close-fullscreen-icon").classList.toggle('display-none');
        document.getElementById("navigation-bar").classList.toggle("display-none");
        document.getElementById("navigation-menu").classList.add("display-none");
        document.getElementById("search").classList.add("display-none");
        document.getElementById("side-bar").classList.toggle("display-none");
        document.getElementById("banners").classList.toggle("display-none");
        document.getElementById("page").classList.toggle("display-none");
        map.updateSize();
    }
    
    function updateGeolocationControl() {
        const control = document.getElementById("geolocation-control");
        const trackingIcon = document.getElementById("geolocation-tracking-icon");
        const enabledIcon = document.getElementById("geolocation-enabled-icon");
        if (geolocationEnabled) {
            control.classList.add("active");
            if (followGeolocation) {
                trackingIcon.classList.remove("display-none");
                enabledIcon.classList.add("display-none");
            } else {
                trackingIcon.classList.add("display-none");
                enabledIcon.classList.remove("display-none");
            }
        } else {
            control.classList.remove("active");
            trackingIcon.classList.remove("display-none");
            enabledIcon.classList.add("display-none");
        }
    }
</script>
