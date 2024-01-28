
% from datetime import timedelta

% from models.date import Date
% from models.model import ModelType

% rebase('base')

% model = bus.model

<div id="page-header">
    <h1 class="row">
        <span>Bus</span>
        % include('components/bus', enable_link=False)
    </h1>
    % if bus.order is None:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % else:
        <h2>{{! bus.order }}</h2>
    % end
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'bus/{bus.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'bus/{bus.number}/history') }}" class="tab-button">History</a>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Realtime Information</h2>
            </div>
            <div class="content">
                % if position is None:
                    <div class="info-box">
                        <div class="section">
                            <h3>Not in service</h3>
                        </div>
                        <div class="row section">
                            <div class="name">Last Seen</div>
                            <div class="value">
                                % if overview is None:
                                    <div class="lighter-text">Never</div>
                                % else:
                                    % last_seen = overview.last_seen_date
                                    % if last_seen.is_today:
                                        <div>Today</div>
                                    % else:
                                        <div>{{ last_seen.format_long() }}</div>
                                        <div class="smaller-font">{{ last_seen.format_since() }}</div>
                                    % end
                                % end
                            </div>
                        </div>
                        % if overview is not None:
                            <div class="row section">
                                <div class="name">System</div>
                                <div class="value">
                                    <a href="{{ get_url(overview.last_seen_system) }}">{{ overview.last_seen_system }}</a>
                                </div>
                            </div>
                        % end
                    </div>
                % elif position.trip is None:
                    % include('components/map', map_position=position)
                    
                    <div class="info-box">
                        <div class="section">
                            <h3>Not in service</h3>
                        </div>
                        % last_record = overview.last_record
                        % if last_record is not None and last_record.date.is_today:
                            % block = last_record.block
                            % if block is not None:
                                % date = Date.today(block.system.timezone)
                                % end_time = block.get_end_time(date=date)
                                % if end_time is not None and end_time.is_later:
                                    <div class="section no-flex">
                                        % include('components/block_timeline', date=date)
                                    </div>
                                % end
                            % end
                        % end
                        <div class="row section">
                            <div class="name">System</div>
                            <div class="value">
                                <a href="{{ get_url(position.system) }}">{{ position.system }}</a>
                            </div>
                        </div>
                        % if show_speed:
                            <div class="row section">
                                <div class="name">Speed</div>
                                <div class="value">{{ position.speed }} km/h</div>
                            </div>
                        % end
                    </div>
                % else:
                    % trip = position.trip
                    % stop = position.stop
                    % block = trip.block
                    % route = trip.route
                    
                    % include('components/map', map_position=position, map_trip=trip, map_departures=trip.find_departures(), zoom_trips=False, zoom_departures=False)
                    
                    <div class="info-box">
                        <div class="section">
                            <div class="row">
                                % include('components/adherence', adherence=position.adherence, size='large')
                                <h3>{{ trip }}</h3>
                            </div>
                        </div>
                        <div class="section">
                            <div class="row">
                                % include('components/route')
                                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                            </div>
                        </div>
                        <div class="section">
                            % include('components/block_timeline', date=Date.today(block.system.timezone))
                        </div>
                        <div class="row section">
                            <div class="name">System</div>
                            <div class="value">
                                <a href="{{ get_url(trip.system) }}">{{ trip.system }}</a>
                            </div>
                        </div>
                        % if show_speed:
                            <div class="row section">
                                <div class="name">Speed</div>
                                <div class="value">{{ position.speed }} km/h</div>
                            </div>
                        % end
                        <div class="row section">
                            <div class="name">Block</div>
                            <div class="value">
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                % date = Date.today(block.system.timezone)
                                % start_time = block.get_start_time(date=date).format_web(time_format)
                                % end_time = block.get_end_time(date=date).format_web(time_format)
                                % duration = block.get_duration(date=date)
                                <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ duration }})</span>
                            </div>
                        </div>
                        <div class="row section">
                            <div class="name">Trip</div>
                            <div class="value">
                                % include('components/trip')
                                % start_time = trip.start_time.format_web(time_format)
                                % end_time = trip.end_time.format_web(time_format)
                                <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ trip.duration }})</span>
                            </div>
                        </div>
                        % if stop is not None:
                            <div class="row section">
                                <div class="name">Next Stop</div>
                                <div class="value">
                                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                    % adherence = position.adherence
                                    % if adherence is not None:
                                        <span class="smaller-font">{{ adherence.description }}</span>
                                    % end
                                </div>
                            </div>
                        % end
                    </div>
                % end
            </div>
        </div>
        
        % if bus.order is not None:
            <div class="section">
                <div class="header">
                    <h2>Details</h2>
                </div>
                <div class="section">
                    <div class="info-box">
                        % if bus.order.size > 1:
                            <div class="section">
                                % include('components/order_details')
                            </div>
                        % end
                        <div class="row section">
                            <div class="name">Vehicle Type</div>
                            <div class="value">{{ model.type }}</div>
                        </div>
                        <div class="row section">
                            <div class="name">Length</div>
                            <div class="value">{{ str(model.length).rstrip('0').rstrip('.') }} feet</div>
                        </div>
                        <div class="row section">
                            <div class="name">Fuel Type</div>
                            <div class="value">{{ model.fuel }}</div>
                        </div>
                    </div>
                </div>
            </div>
        % end
    </div>
    
    <div class="container flex-3">
        % if position is not None:
            % upcoming_departures = position.find_upcoming_departures()
            % if len(upcoming_departures) > 0:
                <div class="section">
                    <div class="header">
                        <h2>Upcoming Stops</h2>
                    </div>
                    <div class="content">
                        % if len([d for d in upcoming_departures if d.timepoint]) > 0:
                            <p>Departures in <span class="timing-point">bold</span> are timing points.</p>
                        % end
                        % if position.adherence is not None and position.adherence.value != 0:
                            <p>Times in brackets are estimates based on current location.</p>
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
                                % for departure in upcoming_departures:
                                    % trip = departure.trip
                                    % stop = departure.stop
                                    <tr>
                                        <td>
                                            <div class="row">
                                                <div class="{{ 'timing-point' if departure.timepoint else '' }}">
                                                    {{ departure.time.format_web(time_format) }}
                                                </div>
                                                % if position.adherence is not None and position.adherence.value != 0:
                                                    % expected_time = departure.time - timedelta(minutes=position.adherence.value)
                                                    <div class="lighter-text">
                                                        ({{ expected_time.format_web(time_format) }})
                                                    </div>
                                                % end
                                            </div>
                                        </td>
                                        % if stop is None:
                                            <td class="lighter-text" colspan="2">Unknown</td>
                                        % else:
                                            <td>
                                                <div class="column">
                                                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a>
                                                    <div class="mobile-only smaller-font {{ 'timing-point' if departure.timepoint else '' }}">{{ stop }}</div>
                                                </div>
                                            </td>
                                            <td class="non-mobile">
                                                <div class="column">
                                                    <div class="{{ 'timing-point' if departure.timepoint else '' }}">{{ stop }}</div>
                                                    % if not departure.pickup_type.is_normal:
                                                        <span class="smaller-font">{{ departure.pickup_type }}</span>
                                                    % elif departure == trip.last_departure:
                                                        <span class="smaller-font">Drop off only</span>
                                                    % end
                                                    % if not departure.dropoff_type.is_normal:
                                                        <span class="smaller-font">{{ departure.dropoff_type }}</span>
                                                    % elif departure == trip.first_departure:
                                                        <span class="smaller-font">Pick up only</span>
                                                    % end
                                                </div>
                                            </td>
                                        % end
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    </div>
                </div>
            % end
        % end
        <div class="section">
            <div class="header">
                <h2>Recent History</h2>
            </div>
            <div class="content">
                % if len(records) == 0:
                    <div class="placeholder">
                        <h3>This bus doesn't have any recorded history</h3>
                        <p>There are a few reasons why that might be the case:</p>
                        <ol>
                            <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                            <li>It may not have been in service since BCTracker started recording bus history</li>
                            <li>It may not have functional NextRide equipment installed</li>
                            % if model is None or model.type == ModelType.shuttle:
                                <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                            % end
                        </ol>
                        <p>Please check again later!</p>
                    </div>
                % else:
                    % if len([r for r in records if len(r.warnings) > 0]) > 0:
                        <p>
                            <span>Entries with a</span>
                            <img class="middle-align white inline" src="/img/white/warning.png" />
                            <img class="middle-align black inline" src="/img/black/warning.png" />
                            <span>may be accidental logins.</span>
                        </p>
                    % end
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th class="desktop-only">System</th>
                                <th>Block</th>
                                <th class="desktop-only">Routes</th>
                                <th class="desktop-only">Start Time</th>
                                <th class="desktop-only">End Time</th>
                                <th class="non-mobile">First Seen</th>
                                <th class="no-wrap">Last Seen</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for record in records:
                                <tr>
                                    <td class="desktop-only">{{ record.date.format_long() }}</td>
                                    <td class="non-desktop">
                                        <div class="column">
                                            {{ record.date.format_short() }}
                                            <span class="smaller-font">{{ record.system }}</span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">{{ record.system }}</td>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % if record.is_available:
                                                    % block = record.block
                                                    <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                                % else:
                                                    <span>{{ record.block_id }}</span>
                                                % end
                                                % include('components/record_warnings')
                                            </div>
                                            <div class="non-desktop">
                                                % include('components/route_list', routes=record.routes)
                                            </div>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/route_list', routes=record.routes)
                                    </td>
                                    <td class="desktop-only">{{ record.start_time.format_web(time_format) }}</td>
                                    <td class="desktop-only">{{ record.end_time.format_web(time_format) }}</td>
                                    <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                    <td>{{ record.last_seen.format_web(time_format) }}</td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                % end
            </div>
        </div>
    </div>
</div>
