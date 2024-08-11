
% import json

% is_preview = get('is_preview', True)

<div id="map" class="{{ 'preview' if is_preview else 'full-screen' }}"></div>

% include('components/svg_script', name='fish')
% include('components/svg_script', name='no-people')
% include('components/svg_script', name='one-person')
% include('components/svg_script', name='two-people')
% include('components/svg_script', name='three-people')

<script>
    const interactive = "{{ is_preview }}" === "False";
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
        interactions: interactive ? ol.interaction.defaults.defaults().extend([
            new ol.interaction.DblClickDragZoom()
        ]) : [],
        controls: ol.control.defaults.defaults({
            zoom: interactive,
            rotate: interactive
        })
    });
    
    const area = new Area();
</script>

% map_trips = get('map_trips', [map_trip] if defined('map_trip') and map_trip else [])
% map_trips = sorted([t for t in map_trips if t.route], key=lambda t: t.route, reverse=True)
% shape_ids = set()
% shape_trips = []
% for trip in map_trips:
    % if trip.shape_id not in shape_ids:
        % shape_ids.add(trip.shape_id)
        % shape_trips.append(trip)
    % end
% end
% if shape_trips:
    <script>
        const trips = JSON.parse('{{! json.dumps([t.get_json() for t in shape_trips]) }}');
        
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
            
            if ("{{ get('zoom_trips', True) }}" === "True") {
                for (const point of trip.points) {
                    area.combine(point.lat, point.lon);
                }
            }
        }
    </script>
% end

% map_positions = get('map_positions', [map_position] if defined('map_position') and map_position else [])
% if map_positions:
    % map_positions = sorted([p for p in map_positions if p.has_location], key=lambda p: p.lat)
    <script>
        const positions = JSON.parse('{{! json.dumps([p.get_json() for p in map_positions]) }}');
        const busMarkerStyle = "{{ bus_marker_style }}";
        
        for (const position of positions) {
            const adherence = position.adherence;
            
            const element = document.createElement("div");
            element.className = "marker";
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
            if (position.adherence !== null && position.adherence !== undefined) {
                headsign.className = "row center gap-5";
                const adherence = position.adherence;
                const adherenceElement = document.createElement("div");
                adherenceElement.classList.add("adherence-indicator", adherence.status_class);
                adherenceElement.innerHTML = adherence.value;
                
                headsign.innerHTML = adherenceElement.outerHTML + position.headsign;
            } else {
                headsign.className = "centred";
                headsign.innerHTML = position.headsign;
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
                element.appendChild(icon);
            }
            
            if (position.adornment != null) {
                title.innerHTML += " <span class='adornment'>" + position.adornment + "</span>";
            }
            
            details.appendChild(title);
            details.appendChild(content);
            element.appendChild(details);
            
            map.addOverlay(new ol.Overlay({
                position: ol.proj.fromLonLat([position.lon, position.lat]),
                positioning: "center-center",
                element: element,
                stopEvent: false
            }));
            
            if ("{{ get('zoom_buses', True) }}" === "True" && position.lat != 0 && position.lon != 0) {
                area.combine(position.lat, position.lon);
            }
        }
    </script>
% end

% map_stops = get('map_stops', [map_stop] if defined('map_stop') and map_stop else [])
% if map_stops:
    % map_stops.sort(key=lambda s: s.lat)
    <script>
        const stops = JSON.parse('{{! json.dumps([s.get_json() for s in map_stops]) }}');
        
        for (const stop of stops) {
            const element = document.createElement("div");
            element.className = "{{ 'marker' if len(map_stops) == 1 else 'marker small' }}";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = getUrl(stop.system_id, "stops/" + stop.number);
            icon.innerHTML = "<div class='link'></div>" + getSVG("stop");
            
            const details = document.createElement("div");
            details.className = "details {{ '' if len(map_stops) == 1 else 'hover-only' }}";
            
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
            
            if ("{{ get('zoom_stops', True) }}" === "True") {
                area.combine(stop.lat, stop.lon);
            }
        }
    </script>
% end

% map_departures = get('map_departures', [map_departure] if defined('map_departure') and map_departure else [])
% map_departures = sorted([d for d in map_departures if d.trip and d.trip.route], key=lambda d: d.trip.route)
% stop_ids = set()
% stop_departures = []
% for departure in map_departures:
    % if departure.stop_id not in stop_ids:
        % stop_ids.add(departure.stop.id)
        % stop_departures.append(departure)
    % end
% end
% if stop_departures:
    % stop_departures.sort(key=lambda d:d.stop.lat)
    <script>
        const departures = JSON.parse('{{! json.dumps([d.get_json() for d in stop_departures]) }}');
        
        for (const departure of departures) {
            const stop = departure.stop;
            
            const element = document.createElement("div");
            element.className = "{{ 'marker' if len(map_departures) == 1 else 'marker small' }}";
            
            const icon = document.createElement("a");
            icon.className = "icon";
            icon.href = getUrl(stop.system_id, "stops/" + stop.number);
            icon.style.backgroundColor = "#" + departure.colour;
            icon.innerHTML = "<div class='link'></div>" + getSVG("stop");
            
            const details = document.createElement("div");
            details.className = "details {{ '' if len(map_departures) == 1 else 'hover-only' }}";
            
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
            
            if ("{{ get('zoom_departures', True) }}" === "True") {
                area.combine(stop.lat, stop.lon);
            }
        }
    </script>
% end

<script>
    document.body.onload = function() {
        map.updateSize();
        if (area.isValid) {
            if (area.isPoint) {
                map.getView().setCenter(ol.proj.fromLonLat(area.point));
                map.getView().setZoom(15);
            } else {
                const padding = parseInt("{{ 20 if is_preview else 100 }}");
                map.getView().fit(ol.proj.transformExtent(area.box, ol.proj.get("EPSG:4326"), ol.proj.get("EPSG:3857")), {
                    padding: [padding, padding, padding, padding]
                })
            }
        }
    }
</script>
