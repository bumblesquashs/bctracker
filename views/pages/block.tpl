% rebase('base', title=f'Block {block.id}')

<div class="page-header">
    <h1 class="title">Block {{ block.id }}</h1>
</div>
<hr />

% services = block.get_services(None)
% routes = block.get_routes(None)
% trips = block.get_trips(None)

<div id="sidebar">
    <h2>Overview</h2>
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
            <div class="value">{{ block.get_start_time(None) }}</div>
        </div>
        <div class="section">
            <div class="name">End time</div>
            <div class="value">{{ block.get_end_time(None) }}</div>
        </div>
        <div class="section">
            <div class="name">Duration</div>
            <div class="value">{{ block.get_duration(None) }}</div>
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
    
    % related_blocks = block.get_related_blocks(None)
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
