
% rebase('base', title=str(route), include_maps=True)

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
    <hr />
</div>

<div class="flex-container">
    % if len(route.trips) > 0:
        <div class="sidebar flex-1">
            <h2>Overview</h2>
            % include('components/map', map_trips=route.trips, map_positions=positions)
            
            <div class="info-box">
                <div class="section no-flex">
                    % include('components/schedule_indicator', schedule=route.schedule)
                </div>
                <div class="section">
                    % headsigns = route.get_headsigns()
                    <div class="name">Headsign{{ '' if len(headsigns) == 1 else 's' }}</div>
                    <div class="value">
                        % for headsign in headsigns:
                            <span>{{ headsign }}</span>
                            <br />
                        % end
                    </div>
                </div>
            </div>
        </div>
    % end
    
    <div class="flex-3">
        % if len(positions) > 0:
            <h2>Active Buses</h2>
            <table class="striped">
                <thead>
                    <tr>
                        <th>Bus</th>
                        <th class="desktop-only">Model</th>
                        <th class="desktop-only">Headsign</th>
                        <th class="desktop-only">Block</th>
                        <th>Trip</th>
                        <th class="non-mobile">Current Stop</th>
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
                                % if order is None:
                                    {{ bus }}
                                % else:
                                    <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                    <br class="non-desktop" />
                                    <span class="non-desktop smaller-font">{{ order }}</span>
                                % end
                            </td>
                            <td class="desktop-only">
                                % if order is not None:
                                    {{ order }}
                                % end
                            </td>
                            <td class="desktop-only">{{ trip }}</td>
                            <td class="desktop-only">
                                % block = trip.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            </td>
                            <td>
                                <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                <br class="non-desktop" />
                                <span class="non-desktop smaller-font">{{ trip }}</span>
                            </td>
                            % if stop is None:
                                <td class="non-mobile lighter-text">Unavailable</td>
                            % else:
                                <td class="non-mobile">
                                    % include('components/adherence_indicator', adherence=position.adherence)
                                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                </td>
                            % end
                        </tr>
                    % end
                </tbody>
            </table>
        % end
        
        <h2>Today's Schedule</h2>
        % if len(trips) == 0:
            <p>
                There are no trips for this route today.
                You can check the <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}">full schedule</a> for more information about when this route runs.
            </p>
        % else:
            % trip_positions = {p.trip.id:p for p in positions if p.trip is not None and p.trip in trips}
            % directions = sorted({t.direction for t in trips})
            <div class="container">
                % for direction in directions:
                    % direction_trips = [t for t in trips if t.direction == direction]
                    % if len(direction_trips) > 0:
                        <div class="section">
                            % if len(directions) > 1:
                                <h3>{{ direction }}</h3>
                            % end
                            
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
                                        <th class="non-mobile">Headsign</th>
                                        <th class="desktop-only">Departing From</th>
                                        <th class="desktop-only">Block</th>
                                        <th>Trip</th>
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
                                            <td>{{ trip.start_time }}</td>
                                            % if system is None or system.realtime_enabled:
                                                % if trip.id in recorded_today:
                                                    % bus = recorded_today[trip.id]
                                                    % order = bus.order
                                                    <td>
                                                        % if trip.id in trip_positions:
                                                            % position = trip_positions[trip.id]
                                                            % include('components/adherence_indicator', adherence=position.adherence)
                                                        % end
                                                        % if order is None:
                                                            {{ bus }}
                                                        % else:
                                                            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                                            <br class="non-desktop" />
                                                            <span class="non-desktop smaller-font">{{ order }}</span>
                                                        % end
                                                    </td>
                                                    <td class="desktop-only">
                                                        % if order is not None:
                                                            {{ order }}
                                                        % end
                                                    </td>
                                                % elif trip.block_id in scheduled_today and trip.start_time.is_later:
                                                    % bus = scheduled_today[trip.block_id]
                                                    % order = bus.order
                                                    <td>
                                                        % if order is None:
                                                            {{ bus }}
                                                        % else:
                                                            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                                        % end
                                                        <span class="tooltip-anchor">
                                                            <img class="middle-align white" src="/img/white/schedule.png" />
                                                            <img class="middle-align black" src="/img/black/schedule.png" />
                                                            <div class="tooltip">Bus is scheduled</div>
                                                        </span>
                                                        % if order is not None:
                                                            <br class="non-desktop" />
                                                            <span class="non-desktop smaller-font">{{ order }}</span>
                                                        % end
                                                    </td>
                                                    <td class="desktop-only">
                                                        % if order is not None:
                                                            {{ order }}
                                                        % end
                                                    </td>
                                                % else:
                                                    <td class="desktop-only lighter-text" colspan="2">Unavailable</td>
                                                    <td class="non-desktop lighter-text">Unavailable</td>
                                                % end
                                            % end
                                            <td class="non-mobile">{{ trip }}</td>
                                            <td class="desktop-only"><a href="{{ get_url(first_stop.system, f'stops/{first_stop.number}') }}">{{ first_stop }}</a></td>
                                            <td class="desktop-only"><a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a></td>
                                            <td>
                                                <a class="trip-id" href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                                <br class="mobile-only" />
                                                <span class="mobile-only smaller-font">{{ trip }}</span>
                                            </td>
                                        </tr>
                                        % if this_hour > last_hour:
                                            % last_hour = this_hour
                                        % end
                                    % end
                                </tbody>
                            </table>
                        </div>
                    % end
                % end
            </div>
        % end
    </div>
</div>

% include('components/top_button')
