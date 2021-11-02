% from formatting import format_date, format_date_mobile
% from models.model import BusModelType

% rebase('base', title=f'Bus {bus}', include_maps=True)

<div class="page-header">
    <h1 class="title">Bus {{ bus }}</h1>
    % order = bus.order
    <h2 class="subtitle">{{ order.year }} {{ order.model }}</h2>
</div>
<hr />

<div id="sidebar">
    <h2>Realtime Information</h2>
    % position = bus.position
    % if not position.active:
        <div class="info-box">
            <h3 class="title">Not in service</h3>
        </div>
    % elif position.trip is None:
        % include('components/bus_map', bus=bus)
        
        <div class="info-box">
            <h3 class="title">Not in service</h3>
        </div>
    % else:
        % include('components/bus_map', bus=bus)
        
        % trip = position.trip
        <div class="info-box">
            <h3 class="title">{{ trip }}</h3>
            
            <div class="section">
                <div class="name">System</div>
                <div class="value">{{ trip.system }}</div>
            </div>
            <div class="section">
                <div class="name">Route</div>
                <div class="value">
                    <a href="{{ get_url(trip.route.system, f'routes/{trip.route.number}') }}">{{ trip.route }}</a>
                </div>
            </div>
            <div class="section">
                <div class="name">Block</div>
                <div class="value">
                    <a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a>
                </div>
            </div>
            <div class="section">
                <div class="name">Trip</div>
                <div class="value">
                    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                </div>
            </div>
            % stop = position.stop
            % if stop is not None:
                <div class="section">
                    <div class="name">Current Stop</div>
                    <div class="value">
                        <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                        % adherence = position.schedule_adherence_string
                        % if adherence is not None:
                            <br />
                            <span class="smaller-font">{{ adherence }}</span>
                        % end
                    </div>
                </div>
            % end
        </div>
    % end
    
    <h2>Details</h2>
    <div class="info-box">
        % order = bus.order
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

<div>
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
        <table class="pure-table pure-table-horizontal pure-table-striped">
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
                </tr>
            </thead>
            <tbody>
                % for record in records:
                    <tr>
                        <td class="desktop-only">{{ format_date(record.date) }}</td>
                        <td class="non-desktop no-wrap">{{ format_date_mobile(record.date) }}</td>
                        <td>{{ record.system }}</td>
                        <td>
                            % if record.is_available:
                                % block = record.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % else:
                                <span>{{ record.block_id }}</span>
                            % end
                            <span class="non-desktop smaller-font">
                                <br />
                                {{ record.routes }}
                            </span>
                        </td>
                        <td class="desktop-only">{{ record.routes }}</td>
                        <td class="desktop-only">{{ record.start_time }}</td>
                        <td class="desktop-only">{{ record.end_time }}</td>
                        <td class="tablet-only">{{ record.start_time }} - {{ record.end_time }}</td>
                    </tr>
                % end
            </tbody>
        </table>
        
        <div class="history-older">
            <a href="{{ get_url(system, f'bus/{bus.number}/history') }}">See all history</a>
        </div>
    % end
</div>