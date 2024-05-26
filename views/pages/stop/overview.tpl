
% from math import floor

% from models.date import Date
% from repositories import PositionRepository

% rebase('base')

<div id="page-header">
    % if stop.is_yard:
        <h1 class="row">
            <span>{{ stop }}</span>
            % include('components/favourite')
        </h1>
    % else:
        <h1 class="row">
            <span>Stop {{ stop.number }}</span>
            % include('components/favourite')
        </h1>
        <h2>{{ stop }}</h2>
    % end
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
                
                % if stop_departures:
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
        
        % alt_systems = [s for s in systems if s.get_stop(number=stop.number) and s != system]
        % if alt_systems:
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
                        % if not system or system.realtime_enabled:
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
                                    % if not system or system.realtime_enabled:
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
                    % else:
                        % tomorrow = Date.today().next()
                        <div class="placeholder">
                            <p>
                                There are no departures for the rest of today.
                                <a href="{{ get_url(stop.system, f'stops/{stop.number}/schedule/{tomorrow.format_db()}') }}">Check tomorrow's schedule.</a>
                            </p>
                        </div>
                    % end
                </div>
            </div>
        % end
        
        % if stop.is_yard and system.realtime_enabled:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Buses</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if buses:
                        % orders = sorted({b.order for b in buses if b.order})
                        % unknown_buses = sorted([b for b in buses if not b.order])
                        <table>
                            <thead>
                                <tr>
                                    <th>Bus</th>
                                    <th>Headsign</th>
                                    <th class="desktop-only">Block</th>
                                    <th class="desktop-only">Trip</th>
                                    <th class="non-mobile">Next Stop</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for order in orders:
                                    % order_buses = sorted([b for b in buses if b.order and b.order == order])
                                    <tr class="header">
                                        <td colspan="5">
                                            <div class="row space-between">
                                                <div>{{! order }}</div>
                                                <div>{{ len(order_buses) }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % for bus in order_buses:
                                        % position = di[PositionRepository].find(bus)
                                        <tr>
                                            <td>
                                                <div class="row">
                                                    % include('components/bus')
                                                    % if position:
                                                        % include('components/adherence', adherence=position.adherence)
                                                    % end
                                                </div>
                                            </td>
                                            % if position and position.trip:
                                                % position_stop = position.stop
                                                <td>
                                                    <div class="column">
                                                        % include('components/headsign', trip=position.trip)
                                                        <div class="non-desktop smaller-font">
                                                            Trip:
                                                            % include('components/trip', include_tooltip=False, trip=position.trip)
                                                        </div>
                                                        % if position_stop:
                                                            <div class="mobile-only smaller-font">
                                                                Next Stop: <a href="{{ get_url(position_stop.system, f'stops/{position_stop.number}') }}">{{ position_stop }}</a>
                                                            </div>
                                                        % end
                                                    </div>
                                                </td>
                                                <td class="desktop-only">
                                                    % block = position.trip.block
                                                    <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                                </td>
                                                <td class="desktop-only">
                                                    % include('components/trip', include_tooltip=False, trip=position.trip)
                                                </td>
                                                <td class="non-mobile">
                                                    % if position_stop:
                                                        <a href="{{ get_url(position_stop.system, f'stops/{position_stop.number}') }}">{{ position_stop }}</a>
                                                    % else:
                                                        <span class="lighter-text">Unavailable</span>
                                                    % end
                                                </td>
                                            % else:
                                                <td class="lighter-text" colspan="4">Not In Service</td>
                                            % end
                                        </tr>
                                    % end
                                % end
                            </tbody>
                        </table>
                    % else:
                        <div class="placeholder">
                            <h3>There are no buses associated with this yard</h3>
                            <p>Please check again later!</p>
                        </div>
                    % end
                </div>
            </div>
        % end
        
        % if departures or not stop.is_yard:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Today's Schedule</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if departures:
                        % if not system or system.realtime_enabled:
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
                                    % if not system or system.realtime_enabled:
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
                    % else:
                        <div class="placeholder">
                            % if system.gtfs_loaded:
                                <h3>There are no departures from this stop today</h3>
                                <p>You can check the <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}">full schedule</a> for more information about when this stop has service.</p>
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
