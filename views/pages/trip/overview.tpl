% rebase('base', title=f'Trip {trip.id}', include_maps=True)

% positions = sorted(trip.positions)

<div class="page-header">
    <h1 class="title">Trip {{ trip.id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'trips/{trip.id}/map') }}" class="tab-button">Map</a>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'trips/{trip.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
    <hr />
</div>

<div class="sidebar">
    <h2>Overview</h2>
    % include('components/map', map_trip=trip, map_buses=[p.bus for p in positions])
    
    <div class="info-box">
        <div class="section">
            % include('components/service_indicator', service=trip.service)
        </div>
        <div class="section">
            <div class="name">Start time</div>
            <div class="value">{{ trip.start_time }}</div>
        </div>
        <div class="section">
            <div class="name">End time</div>
            <div class="value">{{ trip.end_time }}</div>
        </div>
        <div class="section">
            <div class="name">Duration</div>
            <div class="value">{{ trip.duration }}</div>
        </div>
        <div class="section">
            <div class="name">Number of stops</div>
            <div class="value">{{ len(trip.departures) }}</div>
        </div>
        <div class="section">
            <div class="name">Direction</div>
            <div class="value">{{ trip.direction.value }}</div>
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
    </div>
    
    % related_trips = trip.related_trips
    % if len(related_trips) > 0:
        <h2>Related Trips</h2>
        <table class="striped">
            <thead>
                <tr>
                    <th>Trip</th>
                    <th>Block</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for related_trip in related_trips:
                    % block = related_trip.block
                    <tr>
                        <td><a href="{{ get_url(related_trip.system, f'trips/{related_trip.id}') }}">{{ related_trip.id }}</a></td>
                        <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                        <td>{{ related_trip.service.schedule }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
</div>

<div>
    % if len(positions) > 0:
        <h2>Active Bus{{ '' if len(positions) == 1 else 'es' }}</h2>
        <table class="striped">
            <thead>
                <tr>
                    <th>Bus</th>
                    <th class="non-mobile">Model</th>
                    <th>Current Stop</th>
                </tr>
            </thead>
            <tbody>
                % for position in positions:
                    % bus = position.bus
                    % trip = position.trip
                    % stop = position.stop
                    % order = bus.order
                    <tr>
                        <td>
                            % if bus.is_unknown:
                                {{ bus }}
                            % else:
                                <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                            % end
                            % if order is not None:
                                <span class="mobile-only smaller-font">
                                    <br />
                                    {{ order }}
                                </span>
                            % end
                        </td>
                        <td class="non-mobile">
                            % if order is not None:
                                {{ order }}
                            % end
                        </td>
                        % if stop is None:
                            <td class="lighter-text">Unavailable</td>
                        % else:
                            <td>
                                % include('components/adherence_indicator', adherence=position.schedule_adherence)
                                <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                            </td>
                        % end
                    </tr>
                % end
            </tbody>
        </table>
    % end
    
    <h2>Stop Schedule</h2>
    <table class="striped">
        <thead>
            <tr>
                <th>Time</th>
                <th class="non-mobile">Stop Number</th>
                <th class="non-mobile">Stop Name</th>
                <th class="mobile-only">Stop</th>
            </tr>
        </thead>
        <tbody>
            % for departure in trip.departures:
                % stop = departure.stop
                <tr>
                    <td>{{ departure.time }}</td>
                    <td>
                        <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a>
                        <span class="mobile-only smaller-font">
                            <br />
                            {{ stop }}
                        </span>
                    </td>
                    <td class="non-mobile">
                        {{ stop }}
                        % if departure == trip.first_departure:
                            <br />
                            <span class="smaller-font">Loading only</span>
                        % elif departure == trip.last_departure:
                            <br />
                            <span class="smaller-font">Unloading only</span>
                        % end
                    </td>
                </tr>
            % end
        </tbody>
    </table>
</div>
