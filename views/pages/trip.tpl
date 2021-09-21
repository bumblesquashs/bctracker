% rebase('base', title=str(trip), include_maps=True)

<h1>{{ trip }}</h1>
<h2>Trip {{ trip.id }}</h2>
<hr />

<div id="sidebar">
    % include('components/trip_map', trip=trip)
    
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
            <div class="name">Number of stops</div>
            <div class="value">{{ len(trip.stop_times) }}</div>
        </div>
        <div class="section">
            <div class="name">Direction</div>
            <div class="value">{{ trip.direction }}</div>
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
</div>

<div>
    <table class="pure-table pure-table-horizontal pure-table-striped">
        <thead>
            <tr>
                <th>Time</th>
                <th class="non-mobile">Stop Number</th>
                <th class="non-mobile">Stop Name</th>
                <th class="mobile-only">Stop</th>
            </tr>
        </thead>
        <tbody>
            % for stop_time in trip.stop_times:
                <tr>
                    <td>{{ stop_time.time }}</td>
                    <td>
                        <a href="{{ get_url(stop_time.system, f'stops/{stop_time.stop.number}') }}">{{ stop_time.stop.number }}</a>
                        <span class="mobile-only smaller-font">
                            <br />
                            {{ stop_time.stop }}
                        </span>
                    </td>
                    <td class="non-mobile">
                        {{ stop_time.stop }}
                        % if stop_time == trip.first_stop:
                            <br />
                            <span class="smaller-font">Loading only</span>
                        % elif stop_time == trip.last_stop:
                            <br />
                            <span class="smaller-font">Unloading only</span>
                        % end
                    </td>
                </tr>
            % end
        </tbody>
    </table>
</div>
