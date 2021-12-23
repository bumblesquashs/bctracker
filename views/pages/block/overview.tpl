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
</div>
<hr />

% if sheet is None or sheet in block.sheets:
    % services = block.get_services(sheet)
    % routes = block.get_routes(sheet)
    % trips = block.get_trips(sheet)
    % positions = sorted(block.positions)
    
    <div id="sidebar">
        <h2>Overview</h2>
        % include('components/map', map_trips=trips, map_buses=[p.bus for p in positions])
        
        <div class="info-box">
            <div class="section">
                % if len(services) == 1:
                    % include('components/service_indicator', service=services[0])
                % else:
                    % include('components/services_indicator', services=services)
                % end
            </div>
            <div class="section">
                <div class="name">Start time</div>
                <div class="value">{{ block.get_start_time(sheet) }}</div>
            </div>
            <div class="section">
                <div class="name">End time</div>
                <div class="value">{{ block.get_end_time(sheet) }}</div>
            </div>
            <div class="section">
                <div class="name">Duration</div>
                <div class="value">{{ block.get_duration(sheet) }}</div>
            </div>
            <div class="section">
                <div class="name">Number of trips</div>
                <div class="value">{{ len(trips) }}</div>
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
        
        % related_blocks = block.get_related_blocks(sheet)
        % if len(related_blocks) > 0:
            <h2>Related Blocks</h2>
            <table class="pure-table pure-table-horizontal pure-table-striped">
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
                            <td>{{ ', '.join([str(s) for s in related_block.get_services(sheet)]) }}</td>
                        </tr>
                    % end
                </tbody>
            </table>
        % end
    </div>
    
    <div>
        % if len(positions) > 0:
            <h2>Active Bus{{ '' if len(positions) == 1 else 'es' }}</h2>
            <table class="pure-table pure-table-horizontal pure-table-striped">
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
        <table class="pure-table pure-table-horizontal pure-table-striped">
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
                % for trip in trips:
                    <tr>
                        <td>{{ trip.start_time }}</td>
                        <td class="desktop-only">{{ trip.end_time }}</td>
                        <td class="desktop-only">{{ trip.duration }}</td>
                        <td>
                            {{ trip }}
                            <span class="mobile-only smaller-font">
                                <br />
                                {{ trip.direction }}
                            </span>
                        </td>
                        <td class="desktop-only">{{ trip.direction }}</td>
                        <td><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
                    </tr>
                % end
            </tbody>
        </table>
    </div>
% else:
    <p>
        This block is not included in the {{ sheet.value }} sheet.
    </p>
% end