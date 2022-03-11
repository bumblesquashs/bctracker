
% rebase('base', title=str(route), include_maps=True)

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
</div>
<hr />

% services = route.services
% trips = route.trips

% if len(services) > 1:
    % include('components/service_navigation', services=services)
% end

<div class="container">
    
    % for service in services:
        % service_trips = [t for t in trips if t.service == service]
        % directions = {t.direction for t in service_trips}
        <div class="section">
            <h2 class="title" id="service-{{service.id}}">{{ service }}</h2>
            <div class="subtitle">{{ service.date_string }}</div>
            <div class="container">
                % for direction in directions:
                    % direction_trips = [t for t in service_trips if t.direction == direction]
                    <div class="section">
                        % if len(directions) > 1:
                            <h3>{{ direction.value }}</h3>
                        % end
                        <table class="striped">
                            <thead>
                                <tr>
                                    <th class="non-mobile">Start Time</th>
                                    <th class="mobile-only">Start</th>
                                    <th>Headsign</th>
                                    <th class="desktop-only">Departing From</th>
                                    <th class="non-mobile">Block</th>
                                    <th>Trip</th>
                                </tr>
                            </thead>
                            <tbody>
                                % last_hour = -1
                                % for trip in direction_trips:
                                    % first_stop = trip.first_departure.stop
                                    % this_hour = trip.start_time.hour
                                    % if last_hour == -1:
                                        % last_hour = this_hour
                                    % end
                                    <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                        <td>{{ trip.start_time }}</td>
                                        <td>{{ trip }}</td>
                                        <td class="desktop-only"><a href="{{ get_url(first_stop.system, f'stops/{first_stop.number}') }}">{{ first_stop }}</a></td>
                                        <td class="non-mobile"><a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a></td>
                                        <td><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
                                    </tr>
                                    % if this_hour > last_hour:
                                        % last_hour = this_hour
                                    % end
                                % end
                            </tbody>
                        </table>
                    </div>
                % end
            </div>
        </div>
    % end
</div>

% include('components/top_button')
