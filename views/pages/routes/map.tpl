
% import json

% rebase('base')

<div id="page-header">
    <h1>Routes</h1>
    <div class="column gap-10 stretch">
        <div class="tab-button-bar">
            <a href="{{ get_url(system, agency, '/routes') }}" class="tab-button">List</a>
            <span class="tab-button current">Map</span>
        </div>
        % if routes:
            <div class="checkbox-container" onclick="toggleRouteNumbers()">
                <div id="route-numbers-checkbox" class="checkbox {{ 'selected' if show_route_numbers else '' }}">
                    <img class="white" src="/img/white/check.png" />
                    <img class="black" src="/img/black/check.png" />
                </div>
                <span>Show Route Numbers</span>
            </div>
        % end
    </div>
</div>

% if len(routes) == 0:
    <div class="placeholder">
        % if system is None:
            <h3>Route information is unavailable</h3>
            <p>Please check again later!</p>
        % else:
            <h3>Route information for {{ system }} is unavailable</h3>
            % if system.gtfs_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        % end
    </div>
% else:
    <div id="map" class="full-screen display-none"></div>
    <div id="map-loading">
        % include('components/loading')
        <h2>Loading...</h2>
    </div>
    
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
        
        const area = new Area();
        
        let showRouteNumbers = "{{ show_route_numbers }}" !== "False";
        
        function setTrips(trips) {
            for (const trip of trips) {
                map.addLayer(new ol.layer.Vector({
                    source: new ol.source.Vector({
                        features: [
                            new ol.Feature({
                                geometry: new ol.geom.LineString(trip.points.map(function (point) {
                                    return ol.proj.fromLonLat([point.lon, point.lat])
                                })),
                                name: String(trip.shape_id)
                            })
                        ],
                        wrapX: false
                    }),
                    style: new ol.style.Style({
                        stroke: new ol.style.Stroke({
                            color: "#" + trip.colour,
                            width: 4,
                            lineCap: "butt"
                        })
                    })
                }));
                
                for (const point of trip.points) {
                    area.combine(point.lat, point.lon);
                }
            }
        }
        
        function setRouteNumbers(routes) {
            for (const route of routes) {
                const element = document.createElement("div");
                element.classList.add("marker", "route-indicator");
                if (!showRouteNumbers) {
                    element.classList.add("display-none");
                }
                
                const icon = document.createElement("a");
                icon.className = "icon route";
                icon.href = getUrl(route.system_id, route.agency_id, "/routes/" + route.number);
                icon.style.backgroundColor = "#" + route.colour;
                icon.innerHTML = "<div class='link'></div><span class='number'>" + route.number + "</span>";
                
                const details = document.createElement("div");
                details.className = "details hover-only";
                details.innerHTML = "<div class='title'>" + route.name + "</div>";
                
                element.appendChild(icon);
                element.appendChild(details);
                
                map.addOverlay(new ol.Overlay({
                    position: ol.proj.fromLonLat([route.lon, route.lat]),
                    positioning: "center-center",
                    element: element,
                    stopEvent: false
                }));
            }
        }
        
        function toggleRouteNumbers() {
            showRouteNumbers = !showRouteNumbers;
            const checkbox = document.getElementById("route-numbers-checkbox");
            checkbox.classList.toggle("selected");
            setCookie("show_route_numbers", showRouteNumbers ? "true" : "false");
            
            for (const element of document.getElementsByClassName("route-indicator")) {
                if (showRouteNumbers) {
                    element.classList.remove("display-none");
                } else {
                    element.classList.add("display-none");
                }
            }
        }
        
        document.body.onload = function() {
            const request = new XMLHttpRequest();
            request.open("GET", "{{ get_url(system, agency, '/api/routes') }}", true);
            request.responseType = "json";
            request.onload = function() {
                if (request.status === 200) {
                    setTrips(request.response.trips);
                    setRouteNumbers(request.response.indicators);
                    
                    document.getElementById("map").classList.remove("display-none");
                    map.updateSize();
                    if (area.isValid) {
                        if (area.isPoint) {
                            map.getView().setCenter(ol.proj.fromLonLat(area.point));
                            map.getView().setZoom(15);
                        } else {
                            map.getView().fit(ol.proj.transformExtent(area.box, ol.proj.get("EPSG:4326"), ol.proj.get("EPSG:3857")), {
                                padding: [100, 100, 100, 100]
                            });
                        }
                    }
                    stopLoadingInterval();
                    document.getElementById("map-loading").remove();
                }
            };
            request.send();
        }
    </script>

    % include('components/map_toggle')
% end
