% rebase('base', title=f'Stop {stop.number}', include_maps=True)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
</div>
<hr />

% services = stop.get_services(sheet)
% routes = stop.get_routes(sheet)
% departures = stop.get_departures(sheet)

<div id="sidebar">
    <h2>Overview</h2>
    % include('components/stop_map', stop=stop)
    
    <div class="info-box">
        <div class="section">
            % include('components/services_indicator', services=services)
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
    
    % nearby_stops = sorted(stop.get_nearby_stops(sheet))
    % if len(nearby_stops) > 0:
        <h2>Nearby Stops</h2>
        <table class="pure-table pure-table-horizontal pure-table-striped">
            <thead>
                <tr>
                    <th>Number</th>
                    <th>Name</th>
                    <th>Routes</th>
                </tr>
            </thead>
            <tbody>
                % for nearby_stop in nearby_stops:
                    <tr>
                        <td><a href="{{ get_url(nearby_stop.system, f'stops/{nearby_stop.number}') }}">{{ nearby_stop.number }}</a></td>
                        <td>{{ nearby_stop }}</td>
                        <td>{{ nearby_stop.get_routes_string(sheet) }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
</div>

<div>
    <h2>Trip Schedule</h2>
    <div class="container">
        % if len(services) > 1:
            <div class="navigation">
                % for service in services:
                    <a href="#{{service}}" class="button">{{ service }}</a>
                % end
            </div>
            <br />
        % end
        
        % for service in services:
            % service_departures = [d for d in departures if d.trip.service == service]
            
            % if len(service_departures) > 0:
                <div class="section">
                    <h3 class="title" id="{{service}}">{{ service }}</h3>
                    <div class="subtitle">{{ service.date_string }}</div>
                    <table class="pure-table pure-table-horizontal pure-table-striped">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Headsign</th>
                                <th class="desktop-only">Block</th>
                                <th>Trip</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_hour = -1
                            % for departure in service_departures:
                                % trip = departure.trip
                                % block = trip.block
                                % this_hour = departure.time.hour
                                % if last_hour == -1:
                                    % last_hour = this_hour
                                % end
                                <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                    <td>{{ departure.time }}</td>
                                    <td>
                                        {{ trip }}
                                        % if departure == trip.first_departure:
                                            <br />
                                            <span class="smaller-font">Loading only</span>
                                        % elif departure == trip.last_departure:
                                            <br />
                                            <span class="smaller-font">Unloading only</span>
                                        % end
                                    </td>
                                    <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
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
        % end
    </div>
</div>

% include('components/top_button')
