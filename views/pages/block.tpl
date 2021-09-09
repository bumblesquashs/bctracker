% rebase('base', title=f'Block {block.id}')

<h1>Block {{ block.id }}</h1>
<hr />

% services = block.get_services(None)
% routes = block.get_routes(None)
% trips = block.get_trips(None)

<div id="sidebar">
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
</div>

<div>
    <table class="pure-table pure-table-horizontal pure-table-striped">
        <thead>
            <tr>
                <th class="non-mobile">Start Time</th>
                <th class="mobile-only">Start</th>
                <th class="desktop-only">End Time</th>
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
