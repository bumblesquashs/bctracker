
% from math import floor

% import repositories

% rebase('base')

<div id="page-header">
    <h1>Nearby Stops</h1>
</div>

% include('components/svg_script', name='nearby')

% if lat and lon:
    <div class="page-container">
        <div id="current-location" class="sidebar container flex-1">
            <div class="section">
                <div class="header" onclick="toggleSection(this, true)">
                    <h2>Current Location</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % include('components/map', map_stops=stops, preview_padding=50)
                    
                    <script>
                        function showCurrentLocation() {
                            const element = document.createElement("div");
                            element.className = "marker";
                            
                            const icon = document.createElement("div");
                            icon.className = "icon";
                            icon.innerHTML = getSVG("nearby");
                            
                            element.appendChild(icon);
                            
                            const lat = parseFloat("{{ lat }}");
                            const lon = parseFloat("{{ lon }}");
                            
                            map.addOverlay(new ol.Overlay({
                                position: ol.proj.fromLonLat([lon,lat]),
                                positioning: "center-center",
                                element: element,
                                stopEvent: false
                            }));
                            
                            if ("{{ len(stops) }}" === "0") {
                                map.updateSize();
                                map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
                                map.getView().setZoom(17);
                            }
                        }
                        
                        showCurrentLocation();
                    </script>
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
                    <div class="container">
                        % if stops:
                            % for stop in stops:
                                % departures = stop.find_departures(date=today)
                                % routes = {d.trip.route for d in departures if d.trip and d.trip.route}
                                % upcoming_count = 3 + floor(len(routes) / 3)
                                % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
                                % trip_ids = [d.trip_id for d in upcoming_departures]
                                % recorded_today = repositories.record.find_recorded_today(stop.context, trip_ids)
                                % assignments = {a.block_id: a for a in repositories.assignment.find_all(stop.context, stop_id=stop.id)}
                                % positions = {p.trip.id: p for p in repositories.position.find_all(stop.context, trip_id=trip_ids)}
                                <div class="section">
                                    <div class="header" onclick="toggleSection(this)">
                                        <div class="column">
                                            <h3>
                                                % include('components/stop', include_link=False)
                                            </h3>
                                            <div class="row">
                                                % if not context.system:
                                                    <div class="lighter-text">{{ stop.context }}</div>
                                                    <div class="lighter-text">•</div>
                                                % end
                                                <a href="{{ get_url(stop.context, 'stops', stop) }}">View stop schedule and details</a>
                                            </div>
                                        </div>
                                        % include('components/toggle')
                                    </div>
                                    <div class="content">
                                        % if upcoming_departures:
                                            % if context.realtime_enabled:
                                                <p>
                                                    <span>{{ context.vehicle_type_plural }} with a</span>
                                                    <span class="scheduled">
                                                        % include('components/svg', name='schedule')
                                                    </span>
                                                    <span>are scheduled but may be swapped off.</span>
                                                </p>
                                            % end
                                            <table>
                                                <thead>
                                                    <tr>
                                                        <th>Time</th>
                                                        <th class="non-mobile">Headsign</th>
                                                        % if context.enable_blocks:
                                                            <th class="desktop-only">Block</th>
                                                        % end
                                                        <th>Trip</th>
                                                        % if context.realtime_enabled:
                                                            <th>{{ context.vehicle_type }}</th>
                                                            <th class="desktop-only">Model</th>
                                                        % end
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    % last_time = None
                                                    % for departure in upcoming_departures:
                                                        % if not last_time:
                                                            % last_time = departure.time
                                                        % end
                                                        % include('rows/departure', show_divider=departure.time.hour > last_time.hour)
                                                        % last_time = departure.time
                                                    % end
                                                </tbody>
                                            </table>
                                        % else:
                                            % tomorrow = today.next()
                                            <p>
                                                There are no departures for the rest of today.
                                                <a href="{{ get_url(stop.context, 'stops', stop, 'schedule', tomorrow) }}">Check tomorrow's schedule.</a>
                                            </p>
                                        % end
                                    </div>
                                </div>
                            % end
                        % else:
                            <div class="section">
                                <div class="placeholder">
                                    <h3>No stops nearby</h3>
                                    % if context.gtfs_loaded:
                                        <p>You're gonna have to walk!</p>
                                    % else:
                                        <p>System data is currently loading and will be available soon.</p>
                                    % end
                                </div>
                            </div>
                        % end
                    </div>
                </div>
            </div>
        </div>
    </div>
% else:
    % include('components/loading')
    
    <div id="nearby-error" class="display-none">
        % include('components/svg', name='nearby')
        <h2 id="error-title"></h2>
        <p id="error-message"></p>
    </div>
    
    <script>
        function onSuccess(position) {
            window.location.href = getUrl(currentSystemID, "nearby", true, {
                lat: position.coords.latitude,
                lon: position.coords.longitude
            });
        }
        
        function onError(error) {
            stopLoading();
            const code = error.code;
            if (code == error.PERMISSION_DENIED) {
                showError("Access to location is denied", "Give your browser access to your device's location to see nearby stops!");
            } else if (code == error.POSITION_UNAVAILABLE) {
                showError("Location unavailable", "Please try again!");
            } else if (code == error.TIMEOUT) {
                showError("Timed out", "Please try again!");
            } else {
                showError("Unknown error occurred", "Please try again!");
            }
        }
        
        function showError(title, message) {
            document.getElementById("nearby-error").classList.remove("display-none");
            document.getElementById("error-title").innerHTML = title;
            document.getElementById("error-message").innerHTML = message;
        }
        
        startLoading();
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(onSuccess, onError);
        } else {
            showError("Location is not supported", "Make sure you're using a device that has GPS");
        }
    </script>
% end
