% rebase('base', title=f'Block {block.id}', include_maps=True)

<div class="page-header">
    <h1 class="title">Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'blocks/{block.id}/map') }}" class="tab-button">Map</a>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'blocks/{block.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
    <hr />
</div>

% service_groups = block.service_groups
% routes = block.get_routes()
% trips = block.get_trips()
% positions = sorted(block.positions)

<div class="sidebar">
    <h2>Overview</h2>
    % include('components/map', map_trips=trips, map_buses=[p.bus for p in positions])
    
    <div class="info-box">
        <div class="section">
            % include('components/service_group_indicator', service_group=block.service_group)
        </div>
        <div class="section">
            <div class="name">Start time</div>
            <div class="value">
                % for service_group in service_groups:
                    % if len(service_groups) > 1:
                        <div class="smaller-font lighter-text">{{ service_group.schedule }}</div>
                    % end
                    <div>{{ block.get_start_time(service_group) }}</div>
                % end
            </div>
        </div>
        <div class="section">
            <div class="name">End time</div>
            <div class="value">
                % for service_group in service_groups:
                    % if len(service_groups) > 1:
                        <div class="smaller-font lighter-text">{{ service_group.schedule }}</div>
                    % end
                    <div>{{ block.get_end_time(service_group) }}</div>
                % end
            </div>
        </div>
        <div class="section">
            <div class="name">Duration</div>
            <div class="value">
                % for service_group in service_groups:
                    % if len(service_groups) > 1:
                        <div class="smaller-font lighter-text">{{ service_group.schedule }}</div>
                    % end
                    <div>{{ block.get_duration(service_group) }}</div>
                % end
            </div>
        </div>
        <div class="section">
            <div class="name">Number of trips</div>
            <div class="value">
                % for service_group in service_groups:
                    % if len(service_groups) > 1:
                        <div class="smaller-font lighter-text">{{ service_group.schedule }}</div>
                    % end
                    <div>{{ len(block.get_trips(service_group)) }}</div>
                % end
            </div>
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
    
    % related_blocks = block.related_blocks
    % if len(related_blocks) > 0:
        <h2>Related Blocks</h2>
        <table class="striped">
            <thead>
                <tr>
                    <th>Block</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for related_block in related_blocks:
                    <tr>
                        <td><a href="{{ get_url(related_block.system, f'blocks/{related_block.id}') }}">{{ related_block.id }}</a></td>
                        <td>{{ ', '.join([str(s) for s in related_block.services]) }}</td>
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
                    <th class="desktop-only">Model</th>
                    <th>Headsign</th>
                    <th>Trip</th>
                    <th class="non-mobile">Current Stop</th>
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
                        <td>{{ trip }}</td>
                        <td><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
                        % if stop is None:
                            <td class="non-mobile lighter-text">Unavailable</td>
                        % else:
                            <td class="non-mobile">
                                % include('components/adherence_indicator', adherence=position.schedule_adherence)
                                <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                            </td>
                        % end
                    </tr>
                % end
            </tbody>
        </table>
    % end
    
    <h2>Trip Schedule</h2>
    <div class="container">
        % for service_group in service_groups:
            % service_group_trips = block.get_trips(service_group)
            <div class="section">
                % if len(service_groups) > 1:
                    <h3 class="name">{{ service_group.schedule }}</h3>
                % end
                <table class="striped">
                    <thead>
                        <tr>
                            <th class="non-mobile">Start Time</th>
                            <th class="mobile-only">Start</th>
                            <th class="desktop-only">End Time</th>
                            <th class="desktop-only">Duration</th>
                            <th class=>Headsign</th>
                            <th class="desktop-only">Direction</th>
                            <th>Trip</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for trip in service_group_trips:
                            <tr>
                                <td>{{ trip.start_time }}</td>
                                <td class="desktop-only">{{ trip.end_time }}</td>
                                <td class="desktop-only">{{ trip.duration }}</td>
                                <td>
                                    {{ trip }}
                                    <span class="mobile-only smaller-font">
                                        <br />
                                        {{ trip.direction.value }}
                                    </span>
                                </td>
                                <td class="desktop-only">{{ trip.direction.value }}</td>
                                <td><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        % end
    </div>
</div>
