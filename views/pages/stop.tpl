% rebase('base', title=f'Stop {stop.number}', include_maps=True)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
</div>
<hr />

<div id="sidebar">
    <h2>Overview</h2>
    % include('components/stop_map', stop=stop)
    
    <div class="info-box">
        <div class="section">
            % include('components/services_indicator', services=stop.services)
        </div>
        <div class="section">
            <div class="name">Route{{ '' if len(stop.routes) == 1 else 's' }}</div>
            <div class="value">
                % for route in stop.routes:
                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
                <br />
                % end
            </div>
        </div>
    </div>
</div>

<div>
    <h2>Trip Schedule</h2>
    <div class="container">
        % if len(stop.services) > 1:
            <div class="navigation">
                % for service in stop.services:
                    <a href="#{{service}}" class="button">{{ service }}</a>
                % end
            </div>
            <br />
        % end
        
        % for service in stop.services:
            % stop_times = [stop_time for stop_time in stop.stop_times if stop_time.trip.service == service]
            
            % if len(stop_times) > 0:
                <div class="section">
                    <h2 class="title" id="{{service}}">{{ service }}</h2>
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
                            % for stop_time in stop_times:
                                % block = stop_time.trip.block
                                % this_hour = int(stop_time.time.split(':')[0])
                                % if last_hour == -1:
                                    % last_hour = this_hour
                                % end
                                <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                    <td>{{ stop_time.time }}</td>
                                    <td>
                                        {{ stop_time.trip }}
                                        % if stop_time == stop_time.trip.first_stop:
                                            <br />
                                            <span class="smaller-font">Loading only</span>
                                        % elif stop_time == stop_time.trip.last_stop:
                                            <br />
                                            <span class="smaller-font">Unloading only</span>
                                        % end
                                    </td>
                                    <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                    <td><a href="{{ get_url(stop_time.trip.system, f'trips/{stop_time.trip.id}') }}">{{ stop_time.trip.id }}</a></td>
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
