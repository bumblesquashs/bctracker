
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/route')
        <span>{{! route.display_name }}</span>
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(context, 'routes', route, 'map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(context, 'routes', route, 'schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

<div class="page-container">
    % if trips:
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Overview</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % include('components/map', map_trips=trips, map_positions=positions)
                    
                    <div class="info-box">
                        <div class="section">
                            % include('components/sheet_list', sheets=route.sheets, schedule_path=f'routes/{route.url_id}/schedule')
                        </div>
                        <div class="row section">
                            <div class="name">Type</div>
                            <div class="value">{{ route.type }}</div>
                        </div>
                        <div class="column section">
                            % for headsign in route.headsigns:
                                <div>{{ headsign }}</div>
                            % end
                        </div>
                        % if variants:
                            <div class="column gap-5 section">
                                <div class="lighter-text">Route {{ 'Variant' if len(variants) == 1 else 'Variants' }}</div>
                                <div class="column">
                                    % for variant in variants:
                                        <div class="row">
                                            % include('components/route', route=variant)
                                            <a href="{{ get_url(variant.context, 'routes', variant) }}">{{! variant.display_name }}</a>
                                        </div>
                                    % end
                                </div>
                            </div>
                        % end
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
                                                <div class="row gap-5">
                                                    % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                    % include('components/adherence', adherence=position.adherence)
                                                </div>
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
                                            % include('components/headsign', departure=position.departure)
                                            <div class="mobile-only smaller-font">
                                                Trip:
                                                % include('components/trip', include_tooltip=False)
                                            </div>
                                            % if stop:
                                                <div class="non-desktop smaller-font">
                                                    <span class="align-middle">Next Stop:</span>
                                                    % include('components/stop')
                                                </div>
                                            % end
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % block = trip.block
                                        <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/trip')
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/stop')
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
                % if today_trips:
                    % trip_positions = {p.trip.id:p for p in positions if p.trip and p.trip in today_trips}
                    % directions = sorted({t.direction for t in today_trips})
                    <div class="container inline">
                        % for direction in directions:
                            % direction_trips = [t for t in today_trips if t.direction == direction]
                            % if direction_trips:
                                <div class="section">
                                    <div class="header" onclick="toggleSection(this)">
                                        <h3>{{ direction }}</h3>
                                        % include('components/toggle')
                                    </div>
                                    <div class="content">
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
                                                    <th class="non-mobile">Start Time</th>
                                                    <th class="mobile-only">Start</th>
                                                    <th class="desktop-only">Headsign</th>
                                                    <th class="non-mobile">Block</th>
                                                    <th>Trip</th>
                                                    <th class="desktop-only">First Stop</th>
                                                    % if context.realtime_enabled:
                                                        <th>Bus</th>
                                                        <th class="desktop-only">Model</th>
                                                    % end
                                                </tr>
                                            </thead>
                                            <tbody>
                                                % last_start_time = None
                                                % for trip in direction_trips:
                                                    % first_stop = trip.first_stop
                                                    % start_time = trip.start_time
                                                    % if not start_time.is_unknown and not last_start_time:
                                                        % last_start_time = start_time
                                                    % end
                                                    <tr class="{{'divider' if start_time.hour > last_start_time.hour else ''}}">
                                                        <td>{{ trip.start_time.format_web(time_format) }}</td>
                                                        <td class="desktop-only">
                                                            % include('components/headsign')
                                                        </td>
                                                        <td class="non-mobile">
                                                            % block = trip.block
                                                            <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
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
                                                            % include('components/stop', stop=first_stop)
                                                        </td>
                                                        % if context.realtime_enabled:
                                                            % if trip.id in recorded_today:
                                                                % bus = recorded_today[trip.id]
                                                                <td>
                                                                    <div class="column">
                                                                        <div class="row">
                                                                            % include('components/bus')
                                                                            % if trip.id in trip_positions:
                                                                                % position = trip_positions[trip.id]
                                                                                <div class="row gap-5">
                                                                                    % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                                                    % include('components/adherence', adherence=position.adherence)
                                                                                </div>
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
                                                            % elif (trip.context.system_id, trip.block_id) in assignments and trip.end_time.is_later:
                                                                % assignment = assignments[(trip.context.system_id, trip.block_id)]
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
                                                    </tr>
                                                    % last_start_time = start_time
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
                        % if context.gtfs_loaded:
                            <h3>There are no trips for this route today</h3>
                            <p>You can check the <a href="{{ get_url(context, 'routes', route, 'schedule') }}">full schedule</a> for more information about when this route runs.</p>
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
