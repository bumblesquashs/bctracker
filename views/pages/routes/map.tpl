
% import json

% rebase('base')

<div class="page-header">
    <h1 class="title">Routes</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'routes') }}" class="tab-button">List</a>
        <span class="tab-button current">Map</span>
    </div>
</div>

% if system is None:
    <div class="placeholder">
        <p>Choose a system to see individual routes.</p>
        <table class="striped">
            <thead>
                <tr>
                    <th>System</th>
                    <th class="non-mobile"># Routes</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if len(region_systems) > 0:
                        <tr class="section">
                            <td colspan="3">
                                {{ region }}
                            </td>
                        </tr>
                        <tr class="display-none"></tr>
                        % for region_system in region_systems:
                            % count = len(region_system.get_routes())
                            <tr>
                                <td>
                                    <div class="flex-column">
                                        <a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
                                        <span class="mobile-only smaller-font">
                                            % if region_system.is_loaded:
                                                % if count == 1:
                                                    1 Route
                                                % else:
                                                    {{ count }} Routes
                                                % end
                                            % end
                                        </span>
                                    </div>
                                </td>
                                % if region_system.is_loaded:
                                    <td class="non-mobile">{{ count }}</td>
                                    <td>
                                        % include('components/weekdays_indicator', schedule=region_system.schedule, compact=True)
                                    </td>
                                % else:
                                    <td class="lighter-text" colspan="2">Routes are loading...</td>
                                % end
                            </tr>
                        % end
                    % end
                % end
            </tbody>
        </table>
    </div>
% else:
    % if len(routes) == 0:
        <div class="placeholder">
            <h3>Route information for {{ system }} is unavailable</h3>
            % if system.is_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        </div>
    % else:
        <div id="map" class="full-screen"></div>
        
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
                    maxZoom: 18
                }),
                controls: ol.control.defaults.defaults({
                    zoom: false
                })
            });
            
            const lats = [];
            const lons = [];
        </script>
        
        % trips = sorted([t for r in routes for t in r.trips], key=lambda t: t.route, reverse=True)
        % shape_ids = set()
        % shape_trips = []
        % for trip in trips:
            % if trip.shape_id not in shape_ids:
                % shape_ids.add(trip.shape_id)
                % shape_trips.append(trip)
            % end
        % end
        
        % if len(shape_trips) > 0:
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
                    
                    for (const point of trip.points) {
                        lats.push(point.lat);
                        lons.push(point.lon);
                    }
                }
                
                document.body.onload = function() {
                    map.updateSize();
                    if (lons.length === 1 && lats.length === 1) {
                        map.getView().setCenter(ol.proj.fromLonLat([lons[0], lats[0]]));
                        map.getView().setZoom(14);
                    } else if (lons.length > 0 && lats.length > 0) {
                        const minLon = Math.min.apply(Math, lons);
                        const maxLon = Math.max.apply(Math, lons);
                        const minLat = Math.min.apply(Math, lats);
                        const maxLat = Math.max.apply(Math, lats);
                        
                        map.getView().fit(ol.proj.transformExtent([minLon, minLat, maxLon, maxLat], ol.proj.get("EPSG:4326"), ol.proj.get("EPSG:3857")), {
                            padding: [100, 100, 100, 100]
                        })
                    }
                }
            </script>
            
            % routes_json = sorted([j for r in routes for j in r.get_indicator_json()], key=lambda j: j['lat'])
            <script>
                const routes = JSON.parse('{{! json.dumps(routes_json) }}');
                
                for (const route of routes) {
                    const element = document.createElement("div");
                    element.className = "marker";
                    
                    const icon = document.createElement("a");
                    icon.className = "icon route";
                    icon.href = getUrl(route.system_id, "routes/" + route.number);
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
            </script>
        % end
        
        % include('components/map_toggle')
    % end  
% end
