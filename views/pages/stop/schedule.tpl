
% rebase('base', title=f'Stop {stop.number}', include_maps=True)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'stops/{stop.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'stops/{stop.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
</div>
<hr />

% if sheet is None or sheet in stop.sheets:
    % services = stop.get_services(sheet)
    % departures = stop.get_departures(sheet)
    
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
                                % last_hour = this_hour
                            % end
                        </tbody>
                    </table>
                </div>
            % end
        % end
    </div>

    % include('components/top_button')
% else:
    <p>
        This stop is not included in the {{ sheet.value }} sheet.
    </p>
% end
