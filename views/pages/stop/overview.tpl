% rebase('base', title=f'Stop {stop.number}', include_maps=True)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'stops/{stop.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>
<hr />

% if sheet is None or sheet in stop.sheets:
    % services = stop.get_services(sheet)
    % routes = stop.get_routes(sheet)
    % departures = stop.get_departures(sheet)
    
    <div id="sidebar">
        <h2>Overview</h2>
        % include('components/map', map_stop=stop)
        
        <div class="info-box">
            <div class="section">
                % include('components/services_indicator', services=services)
            </div>
            <div class="section">
                <div class="name">Route{{ '' if len(routes) == 1 else 's' }}</div>
                <div class="value">
                    % for route in routes:
                        <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
                        <br />
                    % end
                </div>
            </div>
        </div>
        
        % nearby_stops = sorted(stop.get_nearby_stops(sheet))
        % if len(nearby_stops) > 0:
            <h2>Nearby Stops</h2>
            <table class="striped">
                <thead>
                    <tr>
                        <th>Number</th>
                        <th>Name</th>
                        <th>Routes</th>
                    </tr>
                </thead>
                <tbody>
                    % for nearby_stop in nearby_stops:
                        <tr>
                            <td><a href="{{ get_url(nearby_stop.system, f'stops/{nearby_stop.number}') }}">{{ nearby_stop.number }}</a></td>
                            <td>{{ nearby_stop }}</td>
                            <td>{{ nearby_stop.get_routes_string(sheet) }}</td>
                        </tr>
                    % end
                </tbody>
            </table>
        % end
    </div>
    
    <div>
        <h2>Today's Schedule</h2>
        
        % today_departures = [d for d in departures if d.trip.service.is_today]
        
        % if len(today_departures) == 0:
            There are no departures from this stop today.
            You can check the <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}">full schedule</a> for more information about when this stop has service.
        % else:
            % today_buses = today(stop.system, list({d.trip.block_id for d in today_departures}))
            % recorded_buses = today_buses['recorded']
            % scheduled_buses = today_buses['scheduled']
            
            % if system is None or system.realtime_enabled:
                <p>
                    <span>Buses with a</span>
                    <img class="middle-align light-only" src="/img/schedule.png" />
                    <img class="middle-align dark-only" src="/img/schedule-white.png" />
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
                    % for departure in today_departures:
                        % trip = departure.trip
                        % block = trip.block
                        % this_hour = departure.time.hour
                        % if last_hour == -1:
                            % last_hour = this_hour
                        % end
                        <tr class="{{'divider' if this_hour > last_hour else ''}}">
                            <td>{{ departure.time }}</td>
                            % if system is None or system.realtime_enabled:
                                % if trip.id in recorded_buses:
                                    % bus = recorded_buses[trip.id]
                                    % order = bus.order
                                    % position = bus.position
                                    <td>
                                        % if position.active and position.trip_id == trip.id and position.schedule_adherence is not None:
                                            % include('components/adherence_indicator', adherence=position.schedule_adherence)
                                        % end
                                        % if bus.is_unknown:
                                            {{ bus }}
                                        % else:
                                            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                        % end
                                        % if order is not None:
                                            <span class="non-desktop smaller-font">
                                                <br />
                                                {{ order }}
                                            </span>
                                        % end
                                    </td>
                                    <td class="desktop-only">
                                        % if order is not None:
                                            {{ order }}
                                        % end
                                    </td>
                                % elif trip.block_id in scheduled_buses and trip.start_time.is_later:
                                    % bus = scheduled_buses[trip.block_id]
                                    % order = bus.order
                                    <td>
                                        % if bus.is_unknown:
                                            <span>{{ bus }}</span>
                                        % else:
                                            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                        % end
                                        <img class="middle-align light-only" src="/img/schedule.png" />
                                        <img class="middle-align dark-only" src="/img/schedule-white.png" />
                                        % if order is not None:
                                            <span class="non-desktop smaller-font">
                                                <br />
                                                {{ order }}
                                            </span>
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
                                <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                <span class="mobile-only smaller-font">
                                    <br />
                                    {{ trip }}
                                </span>
                            </td>
                        </tr>
                        % last_hour = this_hour
                    % end
                </tbody>
            </table>
        % end
    </div>

    % include('components/top_button')
% else:
    <p>
        This stop is not included in the {{ sheet.value }} sheet.
    </p>
% end
