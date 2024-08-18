
% from repositories import PositionRepository

% rebase('base')

<div id="page-header">
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

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Overview</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % include('components/map', map_trip=trip, map_positions=positions)
                
                <div class="info-box">
                    <div class="section">
                        % include('components/sheet_list', sheets=trip.sheets)
                    </div>
                    <div class="section">
                        % route = trip.route
                        % if route:
                            <div class="row">
                                % include('components/route')
                                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                            </div>
                        % else:
                            <div class="lighter-text">Unknown Route</div>
                        % end
                    </div>
                    <div class="section">
                        % include('components/block_timeline', block=trip.block)
                    </div>
                    <div class="row section">
                        % block = trip.block
                        <div class="name">Block</div>
                        <div class="value">
                            % if block:
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % else:
                                <span class="lighter-text">Loading</span>
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
                        % km = length / trip.system.agency.distance_scale
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
        % if related_trips:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Related Trips</h2>
                    % include('components/toggle')
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
                                        % include('components/trip', trip=related_trip)
                                    </td>
                                    <td class="non-mobile">
                                        % if block:
                                            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                        % else:
                                            <div class="lighter-text">Unknown</div>
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
        % if positions:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    % if len(positions) == 1:
                        <h2>Active Bus</h2>
                    % else:
                        <h2>Active Buses</h2>
                    % end
                    % include('components/toggle')
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
                                % trip = position.trip
                                % stop = position.stop
                                <tr>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % include('components/bus')
                                                % include('components/adherence', adherence=position.adherence)
                                            </div>
                                            <span class="mobile-only smaller-font">
                                                % include('components/order', order=bus.order)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/order', order=bus.order)
                                    </td>
                                    <td>
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
        % elif assignment and trip.service.schedule.is_today and trip.end_time.is_later:
            % bus = assignment.bus
            % position = di[PositionRepository].find(bus)
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Scheduled Bus</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <p>This bus is currently assigned to this trip's block but may be swapped off before this trip runs.</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="non-mobile">Model</th>
                                <th>Current Headsign</th>
                                <th class="desktop-only">Current Trip</th>
                                <th class="non-mobile">Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <div class="column">
                                        <div class="row">
                                            % include('components/bus')
                                            % if position:
                                                % include('components/adherence', adherence=position.adherence)
                                            % end
                                        </div>
                                        <span class="mobile-only smaller-font">
                                            % include('components/order', order=bus.order)
                                        </span>
                                    </div>
                                </td>
                                <td class="non-mobile">
                                    % include('components/order', order=bus.order)
                                </td>
                                % if position and position.trip:
                                    % stop = position.stop
                                    <td>
                                        <div class="column">
                                            % include('components/headsign', trip=position.trip)
                                            <div class="non-desktop smaller-font">
                                                Trip:
                                                % include('components/trip', include_tooltip=False, trip=position.trip)
                                            </div>
                                            % if stop:
                                                <div class="mobile-only smaller-font">
                                                    Next Stop: <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                                </div>
                                            % end
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/trip', include_tooltip=False, trip=position.trip)
                                    </td>
                                    <td class="non-mobile">
                                        % if stop:
                                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                        % else:
                                            <span class="lighter-text">Unavailable</span>
                                        % end
                                    </td>
                                % else:
                                    <td class="lighter-text" colspan="3">Not In Service</td>
                                % end
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        % end
        
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Stop Schedule</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if [d for d in departures if d.timepoint]:
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
                                        % if not departure.pickup_type.is_normal:
                                            <span class="mobile-only smaller-font">{{ departure.pickup_type }}</span>
                                        % elif departure == departures[-1]:
                                            <span class="mobile-only smaller-font">No pick up</span>
                                        % end
                                        % if not departure.dropoff_type.is_normal:
                                            <span class="mobile-only smaller-font">{{ departure.dropoff_type }}</span>
                                        % elif departure == departures[0]:
                                            <span class="mobile-only smaller-font">No drop off</span>
                                        % end
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
                                            <span class="smaller-font">No pick up</span>
                                        % end
                                        % if not departure.dropoff_type.is_normal:
                                            <span class="smaller-font">{{ departure.dropoff_type }}</span>
                                        % elif departure == departures[0]:
                                            <span class="smaller-font">No drop off</span>
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
