
% from math import floor

% from models.stop import StopType

% import repositories

% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/stop', include_link=False)
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ stop.url('map', routes=routes_query) }}" class="tab-button">Map</a>
        % if stop.type != StopType.STATION:
            <a href="{{ stop.url('schedule', routes=routes_query) }}" class="tab-button">Schedule</a>
        % end
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this, true)">
                <h2>Overview</h2>
                % include('components/toggle')
            </div>
            <div class="content gap-20">
                % stop_departures = stop.find_departures()
                % include('components/map', map_stop=stop, map_trips=[d.trip for d in stop_departures], zoom_trips=False)
                
                % if stop_departures:
                    <div class="info-box">
                        <div class="section">
                            % include('components/sheet_list', sheets=stop.sheets, schedule_path=f'stops/{stop.url_id}/schedule', schedule_path_args={'routes': routes_query})
                        </div>
                        % if parent_stop:
                            <div class="row section">
                                <div class="name">Station</div>
                                <div class="value">
                                    % include('components/stop', stop=parent_stop)
                                </div>
                            </div>
                        % end
                    </div>
                % end
            </div>
        </div>
        
        % if stop.type == StopType.STATION:
            % filter_routes = sorted({r for s in child_stops for r in s.routes})
        % else:
            % filter_routes = stop.routes
        % end
        % show_filters = len(filter_routes) > 1
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Routes</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if show_filters and show_help_text:
                    <p>Select routes to filter schedule.</p>
                % end
                <div class="info-box">
                    % if show_filters:
                        <div class="row section">
                            <div class="lighter-text">
                                % if routes_filter:
                                    % if len(routes_filter) == 1:
                                        1 route selected
                                    % else:
                                        {{ len(routes_filter) }} routes selected
                                    % end
                                % else:
                                    No routes selected
                                % end
                            </div>
                            <button class="button compact" onclick="resetRoutesFilter()">Reset</button>
                        </div>
                    % end
                    <div class="section">
                        <div class="options-container">
                            % for route in filter_routes:
                                <div class="row space-between">
                                    <div class="row">
                                        % include('components/route')
                                        <a href="{{ route.url() }}">{{! route.display_name }}</a>
                                    </div>
                                    % if show_filters:
                                        <div class="option space-between" onclick="toggleRouteFilter('{{ route.url_id }}')">
                                            <div class="checkbox {{ 'selected' if route.url_id in routes_filter else '' }}">
                                                % include('components/svg', name='status/check')
                                            </div>
                                        </div>
                                    % end
                                </div>
                            % end
                        </div>
                    </div>
                </div>
            </div>
            <script>
                const routesFilter = new Set("{{ ','.join(routes_filter) }}".split(",").filter(function(route) {
                    return route !== "";
                }));
                
                function toggleRouteFilter(number) {
                    if (routesFilter.has(number)) {
                        routesFilter.delete(number);
                    } else {
                        routesFilter.add(number);
                    }
                    updateFilters();
                }
                
                function resetRoutesFilter() {
                    routesFilter.clear();
                    updateFilters();
                }
                
                function updateFilters() {
                    window.location = getURL(currentAgencyID, currentSystemID, "stops/{{ stop.url_id }}", {
                        "routes": routesFilter.size === 0 ? null : Array.from(routesFilter).sort().join(","),
                    });
                }
            </script>
        </div>
        
        % if nearby_stops:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Nearby Stops</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Stop</th>
                                <th>Routes</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for nearby_stop in nearby_stops:
                                <tr>
                                    <td>
                                        % include('components/stop', stop=nearby_stop)
                                    </td>
                                    <td>
                                        % include('components/route_list', routes=nearby_stop.routes)
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
        
        % alt_stops = [s.get_stop(number=stop.number) for s in systems if s.get_stop(number=stop.number) and s != context.system and s.agency == context.agency]
        % if alt_stops:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Other Systems At This Stop</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>System</th>
                                <th>Routes</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for alt_stop in alt_stops:
                                <tr>
                                    <td><a href="{{ alt_stop.url() }}">{{ alt_stop.context }}</a></td>
                                    <td>
                                        % include('components/route_list', routes=alt_stop.routes)
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
    </div>
    
    <div class="container flex-3">
        % if child_stops:
            % for child_stop in child_stops:
                % departures = child_stop.find_departures(date=today)
                % if routes_filter:
                    % departures = [d for d in departures if d.trip and d.trip.route and d.trip.route.url_id in routes_filter]
                % end
                <div class="section">
                    <div class="header" onclick="toggleSection(this)">
                        <div class="column">
                            <h2>
                                % include('components/stop', stop=child_stop, include_link=False)
                            </h2>
                            <a href="{{ child_stop.url(routes=routes_query) }}">View stop schedule and details</a>
                        </div>
                        % include('components/toggle')
                    </div>
                    <div class="content">
                        % if departures:
                            % routes = {d.trip.route for d in departures if d.trip and d.trip.route}
                            % upcoming_count = 3 + floor(len(routes) / 3)
                            % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
                            % if upcoming_departures:
                                % trip_ids = [d.trip_id for d in upcoming_departures]
                                % recorded_today = repositories.record.find_recorded_today(child_stop.context, trip_ids)
                                % assignments = {a.block_id: a for a in repositories.assignment.find_all(child_stop.context, stop_id=child_stop.id)}
                                % positions = {p.trip.id: p for p in repositories.position.find_all(child_stop.context, trip_id=trip_ids)}
                                % if context.realtime_enabled and context.enable_realtime_trips and show_help_text:
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
                                            % if context.realtime_enabled and context.enable_realtime_trips:
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
                                            % include('components/departure_row', show_divider=departure.time.hour > last_time.hour)
                                            % last_time = departure.time
                                        % end
                                    </tbody>
                                </table>
                            % else:
                                <p>
                                    There are no departures for the rest of today.
                                    <a href="{{ child_stop.url('schedule', today.next(), routes=routes_query) }}">Check tomorrow's schedule.</a>
                                </p>
                            % end
                        % else:
                            % if routes_filter:
                                <p>There are no departures today for the selected routes.</p>
                            % else:
                                <p>
                                    There are no departures today.
                                    <a href="{{ child_stop.url('schedule', today.next(), routes=routes_query) }}">Check tomorrow's schedule.</a>
                                </p>
                            % end
                        % end
                    </div>
                </div>
            % end
         % else:
            % if routes_filter:
                % departures = [d for d in departures if d.trip and d.trip.route and d.trip.route.url_id in routes_filter]
            % end
            % if departures:
                <div class="section">
                    <div class="header" onclick="toggleSection(this)">
                        <h2>Upcoming Departures</h2>
                        % include('components/toggle')
                    </div>
                    <div class="content">
                        % upcoming_count = 3 + floor(len(stop.routes) / 3)
                        % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
                        % if upcoming_departures:
                            % if context.realtime_enabled and context.enable_realtime_trips and show_help_text:
                                <p>
                                    <span>{{ context.vehicle_type_plural }} with a</span>
                                    <span class="scheduled">
                                        % include('components/svg', name='schedule')
                                    </span>
                                    <span>are scheduled but may be swapped off.</span>
                                </p>
                                <p>Times in brackets are estimates based on current vehicle location.</p>
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
                                        % if context.realtime_enabled and context.enable_realtime_trips:
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
                                        % include('components/departure_row', show_divider=departure.time.hour > last_time.hour, show_time_estimate=True)
                                        % last_time = departure.time
                                    % end
                                </tbody>
                            </table>
                        % else:
                            <div class="placeholder">
                                <p>
                                    There are no departures for the rest of today.
                                    <a href="{{ stop.url('schedule', today.next(), routes=routes_query) }}">Check tomorrow's schedule.</a>
                                </p>
                            </div>
                        % end
                    </div>
                </div>
            % end
            
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Today's Schedule</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if departures:
                        <div class="options-container">
                            <div class="option" onclick="toggleCompactSchedule()">
                                <div class="checkbox {{ 'selected' if compact_schedule else '' }}">
                                    % include('components/svg', name='status/check')
                                </div>
                                <div>Show Compact Schedule</div>
                            </div>
                            <script>
                                function toggleCompactSchedule() {
                                    window.location = "{{! stop.url(compact_schedule='false' if compact_schedule else 'true', routes=routes_query) }}";
                                }
                            </script>
                        </div>
                        % if compact_schedule:
                            % if show_help_text and any([1 for d in departures if d.trip and d.trip.last_departure == d or not d.pickup_type.is_normal]):
                                <p>Departures with a <span class="lighter-text strike-through">line through</span> do not pick up.</p>
                            % end
                            % include('components/departure_board')
                        % else:
                            % if context.realtime_enabled and context.enable_realtime_trips and show_help_text:
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
                                        % if context.realtime_enabled and context.enable_realtime_trips:
                                            <th>{{ context.vehicle_type }}</th>
                                            <th class="desktop-only">Model</th>
                                        % end
                                    </tr>
                                </thead>
                                <tbody>
                                    % last_time = None
                                    % for departure in departures:
                                        % if not last_time:
                                            % last_time = departure.time
                                        % end
                                        % include('components/departure_row', show_divider=departure.time.hour > last_time.hour)
                                        % last_time = departure.time
                                    % end
                                </tbody>
                            </table>
                        % end
                    % else:
                        <div class="placeholder">
                            % if context.gtfs_loaded:
                                % if routes_filter:
                                    <h3>There are no departures from this stop for the selected routes</h3>
                                    <p>Try selecting other routes to see today's service.</p>
                                % else:
                                    <h3>There are no departures from this stop today</h3>
                                    <p>You can check the <a href="{{ stop.url('schedule') }}">full schedule</a> for more information about when this stop has service.</p>
                                % end
                            % else:
                                <h3>Departures for this stop are unavailable</h3>
                                <p>System data is currently loading and will be available soon.</p>
                            % end
                        </div>
                    % end
                </div>
            </div>
        % end
    </div>
</div>

% include('components/top_button')
