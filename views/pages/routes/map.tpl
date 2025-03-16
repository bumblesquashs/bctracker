
% import json

% rebase('base')

<div id="page-header">
    <div class="row">
        <h1 class="flex-1">Routes</h1>
        % if routes:
            % include('components/settings_toggle')
        % end
    </div>
    <div class="column gap-10 stretch">
        <div class="tab-button-bar">
            <a href="{{ get_url(context, 'routes') }}" class="tab-button">List</a>
            <span class="tab-button current">Map</span>
        </div>
    </div>
</div>

% if routes:
    <div id="settings" class="options-container collapsed">
        <div class="option" onclick="toggleRouteNumbers()">
            <div id="route-numbers-checkbox" class="checkbox {{ 'selected' if show_route_numbers else '' }}">
                % include('components/svg', name='status/check')
            </div>
            <span>Show Route Numbers</span>
        </div>
    </div>
    <script>
        document.getElementById("map").classList.add("display-none");
        
        const area = new Area();
        
        let showRouteNumbers = "{{ show_route_numbers }}" !== "False";
        
        function setTrips(trips) {
            for (const trip of trips) {
                map.addLayer(new ol.layer.Vector({
                    className: "ol-layer route-layer",
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
                    }),
                    zIndex: 1
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
                icon.href = getUrl(route.system_id, "routes/" + route.url_id, true);
                icon.style.backgroundColor = "#" + route.colour;
                icon.innerHTML = "<div class='link'></div><span class='number'>" + route.number + "</span>";
                
                const details = document.createElement("div");
                details.className = "details hover-only";
                
                const title = document.createElement("div");
                title.className = "title";
                title.innerHTML = route.name;
                details.appendChild(title);
                
                const agencyLogo = document.createElement("img");
                agencyLogo.className = "agency-logo";
                agencyLogo.src = "/img/agencies/" + route.agency_id + ".png";
                agencyLogo.onerror = function() {
                    agencyLogo.style.visibility = 'hidden';
                };
                
                const content = document.createElement("div");
                content.className = "content";
                details.appendChild(content);
                
                const headsignSection = document.createElement("div");
                headsignSection.className = "column";
                headsignSection.style.width = "fit-content";
                content.appendChild(headsignSection);
                
                for (headsign of route.headsigns.slice(0, 4)) {
                    const headsignRow = document.createElement("div");
                    headsignRow.className = "headsign";
                
                    const routeLine = document.createElement("div");
                    routeLine.className = "route-line";
                    routeLine.style.backgroundColor = "#" + route.colour;
                    
                    headsignRow.innerHTML = routeLine.outerHTML + headsign;
                    
                    headsignSection.appendChild(headsignRow);
                }
                if (route.headsigns.length == 5) {
                    headsignSection.innerHTML += "<i class='lighter-text'>And 1 other</i>";
                } else if (route.headsigns.length > 5) {
                    headsignSection.innerHTML += "<i class='lighter-text'>And " + (route.headsigns.length - 4) + " others</i>";
                }
                
                content.innerHTML += "<div class='row gap-5'>" + agencyLogo.outerHTML + route.system_name + "</div>";
                
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
            startLoading();
            const request = new XMLHttpRequest();
            request.open("GET", "{{ get_url(context, 'api', 'routes') }}", true);
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
                    stopLoading();
                }
            };
            request.send();
        }
    </script>
% else:
    <div class="placeholder">
        % if not context.system:
            <h3>Route information is unavailable</h3>
            <p>Please check again later!</p>
        % else:
            <h3>{{ context.system }} route information is unavailable</h3>
            % if context.system.gtfs_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        % end
    </div>
% end
