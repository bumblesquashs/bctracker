% rebase('base', title=f'Block {block.id}', include_maps=True)

<div class="page-header">
    <h1 class="title">Block {{ block.id }}</h1>
</div>
<hr />

<div id="sidebar">
    <h2>Overview</h2>
    % include('components/block_map', block=block)
    
    <div class="info-box">
        <div class="section">
            % services = block.services
            % if len(services) == 1:
                % include('components/service_indicator', service=services[0])
            % else:
                % include('components/services_indicator', services=services)
            % end
        </div>
        <div class="section">
            <div class="name">Start time</div>
            <div class="value">{{ block.start_time }}</div>
        </div>
        <div class="section">
            <div class="name">End time</div>
            <div class="value">{{ block.end_time }}</div>
        </div>
        <div class="section">
            <div class="name">Duration</div>
            <div class="value">{{ block.duration }}</div>
        </div>
        <div class="section">
            <div class="name">Number of trips</div>
            <div class="value">{{ len(block.available_trips) }}</div>
        </div>
        <div class="section">
            <div class="name">Route{{ '' if len(block.routes) == 1 else 's' }}</div>
            <div class="value">
                % for route in block.routes:
                    <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
                    <br />
                % end
            </div>
        </div>
    </div>
    
    % related_blocks = block.related_blocks
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
                        <td>{{ ', '.join([str(s) for s in related_block.services]) }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
</div>

<div>
    % positions = block.positions
    % if len(positions) > 0:
        <h2>Realtime Information</h2>
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
                    <tr>
                        % if bus.number is None:
                            <td>{{ bus }}</td>
                            <td class="desktop-only"></td>
                        % else:
                            % order = bus.order
                            <td>
                                <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
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
                        % end
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
            % for trip in block.available_trips:
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
