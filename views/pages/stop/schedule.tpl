
% rebase('base', title=f'Stop {stop.number}', include_maps=True)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'stops/{stop.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'stops/{stop.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
    <hr />
</div>

% sheets = stop.sheets
    
% if len(sheets) > 1 or (len(sheets) == 1 and len(sheets[0].service_groups) > 1):
    % include('components/sheet_navigation', sheets=sheets)
% end

<div class="container">
    % for sheet in sheets:
        % for service_group in sheet.service_groups:
            % departures = stop.get_departures(service_group)
            
            <div class="section">
                <h2 class="title" id="{{ hash(service_group) }}">{{ service_group.schedule }}</h2>
                <div class="subtitle">{{ service_group.date_string }}</div>
                <table class="striped">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th class="non-mobile">Headsign</th>
                            <th class="non-mobile">Block</th>
                            <th>Trip</th>
                        </tr>
                    </thead>
                    <tbody>
                        % last_hour = -1
                        % for departure in departures:
                            % trip = departure.trip
                            % block = trip.block
                            % this_hour = departure.time.hour
                            % if last_hour == -1:
                                % last_hour = this_hour
                            % end
                            <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                <td>{{ departure.time }}</td>
                                <td class="non-mobile">
                                    {{ trip }}
                                    % if departure == trip.last_departure:
                                        <br />
                                        <span class="smaller-font">Unloading only</span>
                                    % end
                                </td>
                                <td class="non-mobile"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                <td>
                                    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                    <br />
                                    <span class="mobile-only smaller-font">{{ trip }}</span>
                                    % if departure == trip.last_departure:
                                        <br />
                                        <span class="mobile-only smaller-font">Unloading only</span>
                                    % end
                                </td>
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
