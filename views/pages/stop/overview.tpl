
% rebase('base', title=f'Stop {stop.number}', include_maps=True)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'stops/{stop.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
    <hr />
</div>

<div class="flex-container">
    <div class="sidebar flex-1">
        <h2>Overview</h2>
        % include('components/map', map_stop=stop)
        
        % if len(stop.departures) > 0:
            <div class="info-box">
                <div class="section no-flex">
                    % include('components/schedules_indicator', schedules=[s.schedule for s in stop.sheets], url=get_url(system, f'stops/{stop.number}/schedule'))
                </div>
                <div class="section">
                    % routes = stop.get_routes()
                    <div class="name">Route{{ '' if len(routes) == 1 else 's' }}</div>
                    <div class="value">
                        % for route in routes:
                            <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
                            <br />
                        % end
                    </div>
                </div>
            </div>
        % end
        
        % nearby_stops = sorted(stop.nearby_stops)
        % if len(nearby_stops) > 0:
            <h2>Nearby Stops</h2>
            <table class="striped">
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
                                % include('components/route_indicator', routes=nearby_stop.get_routes())
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        % end
        
        % alt_systems = [s for s in systems if s.get_stop(number=stop.number) is not None and s != system]
        % if len(alt_systems) > 0:
            <h2>Other Systems At This Stop</h2>
            <table class="striped">
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
                                % include('components/route_indicator', routes=alt_stop.get_routes())
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        % end
    </div>
    
    <div class="flex-3">
        <h2>Today's Schedule</h2>
        % if len(departures) == 0:
            <p>
                There are no departures from this stop today.
                You can check the <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}">full schedule</a> for more information about when this stop has service.
            </p>
        % else:
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
                        % trip = departure.trip
                        % block = trip.block
                        % this_hour = departure.time.hour
                        % if last_hour == -1:
                            % last_hour = this_hour
                        % end
                        <tr class="{{'divider' if this_hour > last_hour else ''}}">
                            <td>{{ departure.time.format_web(time_format) }}</td>
                            % if system is None or system.realtime_enabled:
                                % if trip.id in recorded_today:
                                    % bus = recorded_today[trip.id]
                                    % order = bus.order
                                    <td>
                                        % if trip.id in positions:
                                            % position = positions[trip.id]
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
                                            <span>{{ bus }}</span>
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
                            <td class="non-mobile">
                                {{ trip }}
                                % if departure == trip.last_departure:
                                    <br />
                                    <span class="smaller-font">Unloading only</span>
                                % end
                            </td>
                            <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                            <td>
                                <a class="trip-id" href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                <br class="mobile-only" />
                                <span class="mobile-only smaller-font">{{ trip }}</span>
                            </td>
                        </tr>
                        % last_hour = this_hour
                    % end
                </tbody>
            </table>
        % end
    </div>
</div>

% include('components/top_button')
