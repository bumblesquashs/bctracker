
% rebase('base')

<div class="page-header">
    <h1>Trip {{! trip.display_id }}</h1>
    <h2>{{ trip }}</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'trips/{trip.id}/map') }}" class="tab-button">Map</a>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'trips/{trip.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% departures = trip.find_departures()

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Overview</h2>
            </div>
            <div class="content">
                % include('components/map', map_trip=trip, map_positions=positions)
                
                <div class="info-box">
                    <div class="section">
                        % include('components/sheets_indicator', sheets=trip.sheets)
                    </div>
                    <div class="section">
                        % route = trip.route
                        % if route is None:
                            <div class="lighter-text">Unknown Route</div>
                        % else:
                            <div class="row">
                                % include('components/route_indicator')
                                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                            </div>
                        % end
                    </div>
                    <div class="row section">
                        % block = trip.block
                        <div class="name">Block</div>
                        <div class="value">
                            % if block is None:
                                <span class="lighter-text">Loading</span>
                            % else:
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % end
                        </div>
                    </div>
                    <div class="row section">
                        <div class="name">Start time</div>
                        <div class="value">{{ trip.start_time.format_web(time_format) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">End time</div>
                        <div class="value">{{ trip.end_time.format_web(time_format) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Duration</div>
                        <div class="value">{{ trip.duration }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Number of stops</div>
                        <div class="value">{{ len(departures) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Direction</div>
                        <div class="value">{{ trip.direction }}</div>
                    </div>
                    % length = trip.length
                    % if length is not None:
                        % km = length / 1000
                        % hours = (float(trip.end_time.get_minutes() - trip.start_time.get_minutes())) / 60
                        <div class="row section">
                            <div class="name">Length</div>
                            <div class="value">{{ f'{km:.1f}' }}km</div>
                        </div>
                        <div class="row section">
                            <div class="name">Average Speed</div>
                            <div class="value">{{ f'{(km / hours):.1f}' }}km/h</div>
                        </div>
                    % end
                </div>
            </div>
        </div>
        
        % related_trips = trip.related_trips
        % if len(related_trips) > 0:
            <div class="section">
                <div class="header">
                    <h2>Related Trips</h2>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Trip</th>
                                <th class="non-mobile">Block</th>
                                <th>Service Days</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for related_trip in related_trips:
                                % block = related_trip.block
                                <tr>
                                    <td>
                                        % include('components/trip_link', trip=related_trip)
                                    </td>
                                    <td class="non-mobile">
                                        % if block is None:
                                            <div class="lighter-text">Unknown</div>
                                        % else:
                                            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                        % end
                                    </td>
                                    <td>
                                        <div class="column">
                                            % for sheet in related_trip.sheets:
                                                <div>{{ sheet }}</div>
                                                <div class="smaller-font lighter-text">{{ sheet.schedule }}</div>
                                            % end
                                        </div>
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
        % if len(positions) > 0:
            <div class="section">
                <div class="header">
                    % if len(positions) == 1:
                        <h2>Active Bus</h2>
                    % else:
                        <h2>Active Buses</h2>
                    % end
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="non-mobile">Model</th>
                                <th>Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for position in sorted(positions):
                                % bus = position.bus
                                % order = bus.order
                                % trip = position.trip
                                % stop = position.stop
                                <tr>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % include('components/bus', bus=bus)
                                                % include('components/adherence_indicator', adherence=position.adherence)
                                            </div>
                                            <span class="mobile-only smaller-font">
                                                % include('components/order', order=order)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/order', order=order)
                                    </td>
                                    <td>
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
                <h2>Stop Schedule</h2>
            </div>
            <div class="content">
                % if len([d for d in departures if d.timepoint]) > 0:
                    <p>Departures in <span class="timing-point">bold</span> are timing points.</p>
                % end
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th class="non-mobile">Stop Number</th>
                            <th class="non-mobile">Stop Name</th>
                            <th class="mobile-only">Stop</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for departure in departures:
                            % stop = departure.stop
                            <tr>
                                <td class="{{ 'timing-point' if departure.timepoint else '' }}">
                                    {{ departure.time.format_web(time_format) }}
                                </td>
                                <td>
                                    <div class="column">
                                        <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a>
                                        <span class="mobile-only smaller-font {{ 'timing-point' if departure.timepoint else '' }}">{{ stop }}</span>
                                    </div>
                                </td>
                                <td class="non-mobile">
                                    <div class="column">
                                        <span class="{{ 'timing-point' if departure.timepoint else '' }}">
                                            {{ stop }}
                                        </span>
                                        % if not departure.pickup_type.is_normal:
                                            <span class="smaller-font">{{ departure.pickup_type }}</span>
                                        % elif departure == departures[-1]:
                                            <span class="smaller-font">Drop off only</span>
                                        % end
                                        % if not departure.dropoff_type.is_normal:
                                            <span class="smaller-font">{{ departure.dropoff_type }}</span>
                                        % elif departure == departures[0]:
                                            <span class="smaller-font">Pick up only</span>
                                        % end
                                    </div>
                                </td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
