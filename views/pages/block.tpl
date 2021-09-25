% rebase('base', title=f'Block {block.id}')

<div class="page-header">
    <h1 class="title">Block {{ block.id }}</h1>
</div>
<hr />

<div id="sidebar">
    <h2>Overview</h2>
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
    
    % for trip in block.available_trips:
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
                <div class="section">
                    <div class="name">Headsign</div>
                    <div class="value">{{ trip }}</div>
                </div>
                <div class="section">
                    <div class="name">Current Route</div>
                    <div class="value">
                        <a href="{{ get_url(trip.route.system, f'routes/{trip.route.number}') }}">{{ trip.route }}</a>
                    </div>
                </div>
                <div class="section">
                    <div class="name">Current Trip</div>
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
            % break
        % end
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
