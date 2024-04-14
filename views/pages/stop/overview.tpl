
% from math import floor

% from models.date import Date

% rebase('base')

<div id="page-header">
    <h1 class="row">
        <span>Stop {{ stop.number }}</span>
        % include('components/favourite')
    </h1>
    <h2>{{ stop }}</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'stops/{stop.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}" class="tab-button">Schedule</a>
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
                
                % if len(stop_departures) > 0:
                    <div class="info-box">
                        <div class="section">
                            % include('components/sheet_list', sheets=stop.sheets, schedule_path=f'stops/{stop.number}/schedule')
                        </div>
                        <div class="column section">
                            % routes = stop.routes
                            % for route in routes:
                                <div class="row">
                                    % include('components/route')
                                    <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                                </div>
                            % end
                        </div>
                    </div>
                % end
            </div>
        </div>
        
        % nearby_stops = sorted(stop.nearby_stops)
        % if len(nearby_stops) > 0:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Nearby Stops</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Number</th>
                                <th>Name</th>
                                <th class="non-mobile">Routes</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for nearby_stop in nearby_stops:
                                <tr>
                                    <td><a href="{{ get_url(nearby_stop.system, f'stops/{nearby_stop.number}') }}">{{ nearby_stop.number }}</a></td>
                                    <td class="non-mobile">{{ nearby_stop }}</td>
                                    <td>
                                        <div class="mobile-only">{{ nearby_stop }}</div>
                                        % include('components/route_list', routes=nearby_stop.routes)
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
        
        % alt_systems = [s for s in systems if s.get_stop(number=stop.number) is not None and s != system]
        % if len(alt_systems) > 0:
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
                            % for alt_system in alt_systems:
                                % alt_stop = alt_system.get_stop(number=stop.number)
                                <tr>
                                    <td><a href="{{ get_url(alt_system, f'stops/{stop.number}') }}">{{ alt_system }}</a></td>
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
        % if len(departures) > 0:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Upcoming Departures</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % upcoming_count = 3 + floor(len(routes) / 3)
                    % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
                    % if len(upcoming_departures) == 0:
                        % tomorrow = Date.today().next()
                        <div class="placeholder">
                            <p>
                                There are no departures for the rest of today.
                                <a href="{{ get_url(stop.system, f'stops/{stop.number}/schedule/{tomorrow.format_db()}') }}">Check tomorrow's schedule.</a>
                            </p>
                        </div>
                    % else:
                        % if system is None or system.realtime_enabled:
                            <p>
                                <span>Buses with a</span>
                                % include('components/svg', name='schedule')
                                <span>are scheduled but may be swapped off.</span>
                            </p>
                        % end
                        <table>
                            <thead>
                                <tr>
                                    <th>Time</th>
                                    % if system is None or system.realtime_enabled:
                                        <th>Bus</th>
                                        <th class="desktop-only">Model</th>
                                    % end
                                    <th class="non-mobile">Headsign</th>
                                    <th class="desktop-only">Block</th>
                                    <th>Trip</th>
                                </tr>
                            </thead>
                            <tbody>
                                % last_hour = -1
                                % for departure in upcoming_departures:
                                    % this_hour = departure.time.hour
                                    % if last_hour == -1:
                                        % last_hour = this_hour
                                    % end
                                    % include('rows/departure', show_divider=this_hour > last_hour)
                                    % last_hour = this_hour
                                % end
                            </tbody>
                        </table>
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
                % if len(departures) == 0:
                    <div class="placeholder">
                        % if system.gtfs_loaded:
                            <h3>There are no departures from this stop today</h3>
                            <p>You can check the <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}">full schedule</a> for more information about when this stop has service.</p>
                        % else:
                            <h3>Departures for this stop are unavailable</h3>
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
                % else:
                    % if system is None or system.realtime_enabled:
                        <p>
                            <span>Buses with a</span>
                            % include('components/svg', name='schedule')
                            <span>are scheduled but may be swapped off.</span>
                        </p>
                    % end
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                % if system is None or system.realtime_enabled:
                                    <th>Bus</th>
                                    <th class="desktop-only">Model</th>
                                % end
                                <th class="non-mobile">Headsign</th>
                                <th class="desktop-only">Block</th>
                                <th>Trip</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_hour = -1
                            % for departure in departures:
                                % this_hour = departure.time.hour
                                % if last_hour == -1:
                                    % last_hour = this_hour
                                % end
                                % include('rows/departure', show_divider=this_hour > last_hour)
                                % last_hour = this_hour
                            % end
                        </tbody>
                    </table>
                % end
            </div>
        </div>
    </div>
</div>

% include('components/top_button')
