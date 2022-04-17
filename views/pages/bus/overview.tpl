
% from models.model import BusModelType

% import formatting

% rebase('base', title=f'Bus {bus}', include_maps=True, show_refresh_button=True)

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
            </div>
        % else:
            % trip = position.trip
            % stop = position.stop
            % block = trip.block
            % route = trip.route
            
            % include('components/map', map_position=position, map_trip=trip, map_departures=trip.departures, zoom_trips=False, zoom_departures=False)
            
            <div class="info-box">
                <h3 class="title">{{ trip }}</h3>
                
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
                        % service_group = block.today_service_group
                        <span class="smaller-font">{{ block.get_start_time(service_group) }} - {{ block.get_end_time(service_group) }} ({{ block.get_duration(service_group) }})</span>
                    </div>
                </div>
                <div class="section">
                    <div class="name">Trip</div>
                    <div class="value">
                        <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                        <br />
                        <span class="smaller-font">{{ trip.start_time }} - {{ trip.end_time }} ({{ trip.duration }})</span>
                    </div>
                </div>
                % if stop is not None:
                    <div class="section">
                        <div class="name">Current Stop</div>
                        <div class="value">
                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                            % adherence = position.schedule_adherence
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
            <div class="section">
                <div class="name">Vehicle Type</div>
                <div class="value">{{ model.type.value }}</div>
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
                    % if model.type == BusModelType.shuttle:
                        <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                    % end
                </ol>
                Please check again later!
            </p>
        % else:
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
                            <td class="desktop-only">{{ formatting.long(record.date) }}</td>
                            <td class="non-desktop no-wrap">{{ formatting.short(record.date) }}</td>
                            <td>{{ record.system }}</td>
                            <td>
                                % if record.is_available:
                                    % block = record.block
                                    <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                % else:
                                    <span>{{ record.block_id }}</span>
                                % end
                                <br />
                                <span class="non-desktop smaller-font">{{ record.routes }}</span>
                            </td>
                            <td class="desktop-only">{{ record.routes }}</td>
                            <td class="desktop-only">{{ record.start_time }}</td>
                            <td class="desktop-only">{{ record.end_time }}</td>
                            <td class="tablet-only">{{ record.start_time }} - {{ record.end_time }}</td>
                            <td class="desktop-only">{{ record.first_seen }}</td>
                            <td class="desktop-only">{{ record.last_seen }}</td>
                        </tr>
                    % end
                </tbody>
            </table>
        % end
    </div>
</div>
