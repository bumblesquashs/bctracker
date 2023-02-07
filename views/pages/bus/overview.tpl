
% from models.date import Date
% from models.model import ModelType

% rebase('base', title=f'Bus {bus}', include_maps=True)

<div class="page-header">
    <h1 class="title">Bus {{ bus }}</h1>
    <h2 class="subtitle">{{ bus.order }}</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'bus/{bus.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'bus/{bus.number}/history') }}" class="tab-button">History</a>
    </div>
    <hr />
</div>

<div class="flex-container">
    <div class="sidebar flex-1">
        <h2>Realtime Information</h2>
        % if position is None:
            <div class="info-box">
                <h3 class="title">Not in service</h3>
            </div>
        % elif position.trip is None:
            % include('components/map', map_position=position)
            
            <div class="info-box">
                <h3 class="title">Not in service</h3>
                
                <div class="section">
                    <div class="name">System</div>
                    <div class="value">{{ position.system }}</div>
                </div>
            </div>
        % else:
            % trip = position.trip
            % stop = position.stop
            % block = trip.block
            % route = trip.route
            
            % include('components/map', map_position=position, map_trip=trip, map_departures=trip.departures, zoom_trips=False, zoom_departures=False)
            
            <div class="info-box">
                <h3 class="title">
                    <div class="flex-row">
                        % include('components/adherence_indicator', adherence=position.adherence, size='large')
                        <div class="flex-1">{{ trip }}</div>
                    </div>
                </h3>
                
                <div class="section">
                    <div class="name">System</div>
                    <div class="value">{{ trip.system }}</div>
                </div>
                <div class="section">
                    <div class="name">Route</div>
                    <div class="value">
                        <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
                    </div>
                </div>
                <div class="section">
                    <div class="name">Block</div>
                    <div class="value">
                        <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                        <br />
                        % if system is None:
                            % today = Date.today(None)
                        % else:
                            % today = Date.today(system.timezone)
                        % end
                        % start_time = block.get_start_time(date=today).format_web(time_format)
                        % end_time = block.get_end_time(date=today).format_web(time_format)
                        % duration = block.get_duration(date=today)
                        <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ duration }})</span>
                    </div>
                </div>
                <div class="section">
                    <div class="name">Trip</div>
                    <div class="value">
                        <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                        <br />
                        % start_time = trip.start_time.format_web(time_format)
                        % end_time = trip.end_time.format_web(time_format)
                        <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ trip.duration }})</span>
                    </div>
                </div>
                % if stop is not None:
                    <div class="section">
                        <div class="name">Current Stop</div>
                        <div class="value">
                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                            % adherence = position.adherence
                            % if adherence is not None:
                                <br />
                                <span class="smaller-font">{{ adherence.description }}</span>
                            % end
                        </div>
                    </div>
                % end
                % if show_speed:
                    <div class="section">
                        <div class="name">Speed</div>
                        <div class="value">{{ position.speed }} km/h</div>
                    </div>
                % end
            </div>
        % end
        
        <h2>Details</h2>
        <div class="info-box">
            % model = bus.model
            % if bus.order.size > 1:
                <div class="section no-flex">
                    % include('components/order_indicator', bus=bus)
                </div>
            % end
            <div class="section">
                <div class="name">Vehicle Type</div>
                <div class="value">{{ model.type }}</div>
            </div>
            <div class="section">
                <div class="name">Length</div>
                <div class="value">{{ str(model.length).rstrip('0').rstrip('.') }} feet</div>
            </div>
            <div class="section">
                <div class="name">Fuel Type</div>
                <div class="value">{{ model.fuel }}</div>
            </div>
        </div>
    </div>
    
    <div class="flex-3">
        <h2>Recent History</h2>
        % if len(records) == 0:
            <p>This bus doesn't have any recorded history.</p>
            <p>
                There are a few reasons why that might be the case:
                <ol>
                    <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                    <li>It may not have been in service since BCTracker started recording bus history</li>
                    <li>It may not have functional NextRide equipment installed</li>
                    % if model.type == ModelType.shuttle:
                        <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                    % end
                </ol>
                Please check again later!
            </p>
        % else:
            % if len([r for r in records if r.is_suspicious]) > 0:
                <p>
                    <span>Blocks with a</span>
                    <img class="middle-align white inline" src="/img/white/warning.png" />
                    <img class="middle-align black inline" src="/img/black/warning.png" />
                    <span>may be accidental logins.</span>
                </p>
            % end
            <table class="striped">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>System</th>
                        <th class="desktop-only">Assigned Block</th>
                        <th class="desktop-only">Assigned Routes</th>
                        <th class="desktop-only">Start Time</th>
                        <th class="desktop-only">End Time</th>
                        <th class="non-desktop">Block</th>
                        <th class="tablet-only">Time</th>
                        <th class="desktop-only">First Seen</th>
                        <th class="desktop-only">Last Seen</th>
                    </tr>
                </thead>
                <tbody>
                    % for record in records:
                        <tr>
                            <td class="desktop-only">{{ record.date.format_long() }}</td>
                            <td class="non-desktop no-wrap">{{ record.date.format_short() }}</td>
                            <td>{{ record.system }}</td>
                            <td>
                                % if record.is_available:
                                    % block = record.block
                                    <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                % else:
                                    <span>{{ record.block_id }}</span>
                                % end
                                % include('components/suspicious_record_indicator', record=record)
                                <br class="non-desktop" />
                                <span class="non-desktop smaller-font">
                                    % include('components/route_indicator', routes=record.routes)
                                </span>
                            </td>
                            % start_time = record.start_time.format_web(time_format)
                            % end_time = record.end_time.format_web(time_format)
                            <td class="desktop-only">
                                % include('components/route_indicator', routes=record.routes)
                            </td>
                            <td class="desktop-only">{{ start_time }}</td>
                            <td class="desktop-only">{{ end_time }}</td>
                            <td class="tablet-only">{{ start_time }} - {{ end_time }}</td>
                            <td class="desktop-only">{{ record.first_seen.format_web(time_format) }}</td>
                            <td class="desktop-only">{{ record.last_seen.format_web(time_format) }}</td>
                        </tr>
                    % end
                </tbody>
            </table>
        % end
    </div>
</div>
