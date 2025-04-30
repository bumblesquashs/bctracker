
% from math import floor

% from models.date import Date

% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/stop', include_link=False)
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(context, 'stops', stop, 'map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(context, 'stops', stop, 'schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Overview</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % stop_departures = stop.find_departures()
                % include('components/map', map_stop=stop, map_trips=[d.trip for d in stop_departures], zoom_trips=False)
                
                % if stop_departures:
                    <div class="info-box">
                        <div class="section">
                            % include('components/sheet_list', sheets=stop.sheets, schedule_path=f'stops/{stop.url_id}/schedule')
                        </div>
                        <div class="column section">
                            % routes = stop.routes
                            % for route in routes:
                                <div class="row">
                                    % include('components/route')
                                    <a href="{{ get_url(route.context, 'routes', route) }}">{{! route.display_name }}</a>
                                </div>
                            % end
                        </div>
                    </div>
                % end
            </div>
        </div>
        
        % nearby_stops = sorted(stop.nearby_stops)
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
                                    <td><a href="{{ get_url(alt_stop.system, 'stops', alt_stop) }}">{{ alt_stop.system }}</a></td>
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
        % if departures:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Upcoming Departures</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % upcoming_count = 3 + floor(len(routes) / 3)
                    % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
                    % if upcoming_departures:
                        % if context.realtime_enabled:
                            <p>
                                <span>Buses with a</span>
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
                                    <th class="desktop-only">Block</th>
                                    <th>Trip</th>
                                    % if context.realtime_enabled:
                                        <th>Bus</th>
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
                                    % include('rows/departure', show_divider=departure.time.hour > last_time.hour, show_time_estimate=True)
                                    % last_time = departure.time
                                % end
                            </tbody>
                        </table>
                    % else:
                        % tomorrow = Date.today().next()
                        <div class="placeholder">
                            <p>
                                There are no departures for the rest of today.
                                <a href="{{ get_url(stop.context, 'stops', stop, 'schedule', tomorrow) }}">Check tomorrow's schedule.</a>
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
                    % if context.realtime_enabled:
                        <p>
                            <span>Buses with a</span>
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
                                <th class="desktop-only">Block</th>
                                <th>Trip</th>
                                % if context.realtime_enabled:
                                    <th>Bus</th>
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
                                % include('rows/departure', show_divider=departure.time.hour > last_time.hour)
                                % last_time = departure.time
                            % end
                        </tbody>
                    </table>
                % else:
                    <div class="placeholder">
                        % if context.system.gtfs_loaded:
                            <h3>There are no departures from this stop today</h3>
                            <p>You can check the <a href="{{ get_url(stop.context, 'stops', stop, 'schedule') }}">full schedule</a> for more information about when this stop has service.</p>
                        % else:
                            <h3>Departures for this stop are unavailable</h3>
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>

% include('components/top_button')
