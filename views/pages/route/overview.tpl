
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/route')
        <span>{{! route.display_name }}</span>
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

<div class="page-container">
    % if route.trips:
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Overview</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % include('components/map', map_trips=route.trips, map_positions=positions)
                    
                    <div class="info-box">
                        <div class="section">
                            % include('components/sheet_list', sheets=route.sheets, schedule_path=f'routes/{route.number}/schedule')
                        </div>
                        <div class="column section">
                            % headsigns = route.get_headsigns()
                            % for headsign in headsigns:
                                <div>{{ headsign }}</div>
                            % end
                        </div>
                    </div>
                </div>
            </div>
        </div>
    % end
    
    <div class="container flex-3">
        % if positions:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Active Buses</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="desktop-only">Model</th>
                                <th>Headsign</th>
                                <th class="non-mobile">Block</th>
                                <th class="non-mobile">Trip</th>
                                <th class="desktop-only">Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for position in positions:
                                % bus = position.bus
                                % trip = position.trip
                                % stop = position.stop
                                <tr>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % include('components/bus')
                                                % include('components/adherence', adherence=position.adherence)
                                            </div>
                                            <span class="non-desktop smaller-font">
                                                % include('components/order', order=bus.order)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/order', order=bus.order)
                                    </td>
                                    <td>
                                        <div class="column">
                                            % include('components/headsign')
                                            <div class="mobile-only smaller-font">
                                                Trip:
                                                % include('components/trip', include_tooltip=False)
                                            </div>
                                            % if stop:
                                                <div class="non-desktop smaller-font">
                                                    Next Stop: <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                                </div>
                                            % end
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % block = trip.block
                                        <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/trip')
                                    </td>
                                    <td class="desktop-only">
                                        % if stop:
                                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                        % else:
                                            <span class="lighter-text">Unavailable</span>
                                        % end
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
        
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Today's Schedule</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if trips:
                    % trip_positions = {p.trip.id:p for p in positions if p.trip and p.trip in trips}
                    % directions = sorted({t.direction for t in trips})
                    <div class="container inline">
                        % for direction in directions:
                            % direction_trips = [t for t in trips if t.direction == direction]
                            % if direction_trips:
                                <div class="section">
                                    <div class="header" onclick="toggleSection(this)">
                                        <h3>{{ direction }}</h3>
                                        % include('components/toggle')
                                    </div>
                                    <div class="content">
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
                                                    <th class="non-mobile">Start Time</th>
                                                    <th class="mobile-only">Start</th>
                                                    % if not system or system.realtime_enabled:
                                                        <th>Bus</th>
                                                        <th class="desktop-only">Model</th>
                                                    % end
                                                    <th class="desktop-only">Headsign</th>
                                                    <th class="non-mobile">Block</th>
                                                    <th>Trip</th>
                                                    <th class="desktop-only">First Stop</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                % last_hour = -1
                                                % for trip in direction_trips:
                                                    % first_stop = trip.first_stop
                                                    % this_hour = trip.start_time.hour
                                                    % if last_hour == -1:
                                                        % last_hour = this_hour
                                                    % end
                                                    <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                                        <td>{{ trip.start_time.format_web(time_format) }}</td>
                                                        % if not system or system.realtime_enabled:
                                                            % if trip.id in recorded_today:
                                                                % bus = recorded_today[trip.id]
                                                                <td>
                                                                    <div class="column">
                                                                        <div class="row">
                                                                            % include('components/bus')
                                                                            % if trip.id in trip_positions:
                                                                                % position = trip_positions[trip.id]
                                                                                % include('components/adherence', adherence=position.adherence)
                                                                            % end
                                                                        </div>
                                                                        <span class="non-desktop smaller-font">
                                                                            % include('components/order', order=bus.order)
                                                                        </span>
                                                                    </div>
                                                                </td>
                                                                <td class="desktop-only">
                                                                    % include('components/order', order=bus.order)
                                                                </td>
                                                            % elif (trip.system.id, trip.block_id) in assignments and trip.end_time.is_later:
                                                                % assignment = assignments[(trip.system.id, trip.block_id)]
                                                                % bus = assignment.bus
                                                                <td>
                                                                    <div class="column">
                                                                        <div class="row">
                                                                            % include('components/bus')
                                                                            % include('components/scheduled')
                                                                        </div>
                                                                        <span class="non-desktop smaller-font">
                                                                            % include('components/order', order=bus.order)
                                                                        </span>
                                                                    </div>
                                                                </td>
                                                                <td class="desktop-only">
                                                                    % include('components/order', order=bus.order)
                                                                </td>
                                                            % else:
                                                                <td class="desktop-only lighter-text" colspan="2">Unavailable</td>
                                                                <td class="non-desktop lighter-text">Unavailable</td>
                                                            % end
                                                        % end
                                                        <td class="desktop-only">
                                                            % include('components/headsign')
                                                        </td>
                                                        <td class="non-mobile">
                                                            <a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a>
                                                        </td>
                                                        <td>
                                                            <div class="column">
                                                                % include('components/trip')
                                                                <span class="non-desktop smaller-font">
                                                                    % include('components/headsign')
                                                                </span>
                                                            </div>
                                                        </td>
                                                        <td class="desktop-only">
                                                            <a href="{{ get_url(first_stop.system, f'stops/{first_stop.number}') }}">{{ first_stop }}</a>
                                                        </td>
                                                    </tr>
                                                    % if this_hour > last_hour:
                                                        % last_hour = this_hour
                                                    % end
                                                % end
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            % end
                        % end
                    </div>
                % else:
                    <div class="placeholder">
                        % if system.gtfs_loaded:
                            <h3>There are no trips for this route today</h3>
                            <p>You can check the <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}">full schedule</a> for more information about when this route runs.</p>
                        % else:
                            <h3>Trips for this route are unavailable</h3>
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>

% include('components/top_button')
