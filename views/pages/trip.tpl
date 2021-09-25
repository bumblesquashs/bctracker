% rebase('base', title=f'Trip {trip.id}', include_maps=True)

<div class="page-header">
    <h1 class="title">Trip {{ trip.id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
</div>
<hr />

<div id="sidebar">
    <h2>Overview</h2>
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
            <div class="name">Duration</div>
            <div class="value">{{ trip.duration }}</div>
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
    
    % position = trip.position
    % if position is not None:
        <h2>Realtime Information</h2>
        <div class="info-box">
            <div class="section">
                % bus = position.bus
                <div class="name">Bus</div>
                <div class="value">
                    % if bus.number is None:
                        {{ bus }}
                    % else:
                        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                        % order = bus.order
                        % if order is not None:
                            <br />
                            <span class="non-desktop smaller-font">{{ order }}</span>
                        % end
                    % end
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
</div>

<div>
    <h2>Stop Schedule</h2>
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
