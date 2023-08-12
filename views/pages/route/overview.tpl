
% rebase('base')

<div class="page-header">
    <h1 class="title">
        <div class="flex-row">
            % include('components/route_indicator')
            <div class="flex-1">{{! route.display_name }}</div>
        </div>
    </h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

<div class="flex-container">
    % if len(route.trips) > 0:
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header">
                    <h2>Overview</h2>
                </div>
                <div class="content">
                    % include('components/map', map_trips=route.trips, map_positions=positions)
                    
                    <div class="info-box">
                        <div class="section no-flex">
                            % include('components/schedules_indicator', schedules=[s.schedule for s in route.sheets], schedule_path=f'routes/{route.number}/schedule')
                        </div>
                        <div class="section vertical">
                            % headsigns = route.get_headsigns()
                            <div class="flex-column">
                                % for headsign in headsigns:
                                    <div>{{ headsign }}</div>
                                % end
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    % end
    
    <div class="container flex-3">
        % if len(positions) > 0:
            <div class="section">
                <div class="header">
                    <h2>Active Buses</h2>
                </div>
                <div class="content">
                    <table class="striped">
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
                                % order = bus.order
                                % trip = position.trip
                                % stop = position.stop
                                <tr>
                                    <td>
                                        <div class="flex-column">
                                            <div class="flex-row left">
                                                % include('components/bus', bus=bus)
                                                % include('components/adherence_indicator', adherence=position.adherence)
                                            </div>
                                            <span class="non-desktop smaller-font">
                                                % include('components/order', order=order)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/order', order=order)
                                    </td>
                                    <td>
                                        <div class="flex-column">
                                            % include('components/headsign_indicator')
                                            <div class="mobile-only smaller-font">
                                                Trip: <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
                                            </div>
                                            % if stop is not None:
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
                                        <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
                                    </td>
                                    <td class="desktop-only">
                                        % if stop is None:
                                            <span class="lighter-text">Unavailable</span>
                                        % else:
                                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
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
            <div class="header">
                <h2>Today's Schedule</h2>
            </div>
            <div class="content">
                % if len(trips) == 0:
                    <p>
                        There are no trips for this route today.
                        You can check the <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}">full schedule</a> for more information about when this route runs.
                    </p>
                % else:
                    % trip_positions = {p.trip.id:p for p in positions if p.trip is not None and p.trip in trips}
                    % directions = sorted({t.direction for t in trips})
                    <div class="container inline">
                        % for direction in directions:
                            % direction_trips = [t for t in trips if t.direction == direction]
                            % if len(direction_trips) > 0:
                                <div class="section">
                                    <div class="header">
                                        <h3>{{ direction }}</h3>
                                    </div>
                                    <div class="content">
                                        % if system is None or system.realtime_enabled:
                                            <p>
                                                <span>Buses with a</span>
                                                <img class="middle-align white" src="/img/white/schedule.png" />
                                                <img class="middle-align black" src="/img/black/schedule.png" />
                                                <span>are scheduled but may be swapped off.</span>
                                            </p>
                                        % end
                                        <table class="striped">
                                            <thead>
                                                <tr>
                                                    <th class="non-mobile">Start Time</th>
                                                    <th class="mobile-only">Start</th>
                                                    % if system is None or system.realtime_enabled:
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
                                                    % first_stop = trip.first_departure.stop
                                                    % this_hour = trip.start_time.hour
                                                    % if last_hour == -1:
                                                        % last_hour = this_hour
                                                    % end
                                                    <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                                        <td>{{ trip.start_time.format_web(time_format) }}</td>
                                                        % if system is None or system.realtime_enabled:
                                                            % if trip.id in recorded_today:
                                                                % bus = recorded_today[trip.id]
                                                                % order = bus.order
                                                                <td>
                                                                    <div class="flex-column">
                                                                        <div class="flex-row left">
                                                                            % include('components/bus', bus=bus)
                                                                            % if trip.id in trip_positions:
                                                                                % position = trip_positions[trip.id]
                                                                                % include('components/adherence_indicator', adherence=position.adherence)
                                                                            % end
                                                                        </div>
                                                                        <span class="non-desktop smaller-font">
                                                                            % include('components/order', order=order)
                                                                        </span>
                                                                    </div>
                                                                </td>
                                                                <td class="desktop-only">
                                                                    % include('components/order', order=order)
                                                                </td>
                                                            % elif trip.block_id in scheduled_today and trip.start_time.is_later:
                                                                % bus = scheduled_today[trip.block_id]
                                                                % order = bus.order
                                                                <td>
                                                                    <div class="flex-column">
                                                                        <div class="flex-row left">
                                                                            % include('components/bus', bus=bus)
                                                                            <div class="tooltip-anchor">
                                                                                <img class="middle-align white" src="/img/white/schedule.png" />
                                                                                <img class="middle-align black" src="/img/black/schedule.png" />
                                                                                <div class="tooltip">Bus is scheduled</div>
                                                                            </div>
                                                                        </div>
                                                                        <span class="non-desktop smaller-font">
                                                                            % include('components/order', order=order)
                                                                        </span>
                                                                    </div>
                                                                </td>
                                                                <td class="desktop-only">
                                                                    % include('components/order', order=order)
                                                                </td>
                                                            % else:
                                                                <td class="desktop-only lighter-text" colspan="2">Unavailable</td>
                                                                <td class="non-desktop lighter-text">Unavailable</td>
                                                            % end
                                                        % end
                                                        <td class="desktop-only">
                                                            % include('components/headsign_indicator')
                                                        </td>
                                                        <td class="non-mobile">
                                                            <a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a>
                                                        </td>
                                                        <td>
                                                            <div class="flex-column">
                                                                <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
                                                                <span class="non-desktop smaller-font">
                                                                    % include('components/headsign_indicator')
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
                % end
            </div>
        </div>
    </div>
</div>

% include('components/top_button')
