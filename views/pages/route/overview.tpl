% from datetime import datetime
% from formatting import format_date

% rebase('base', title=str(route), include_maps=True)

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>
<hr />

% if sheet is None or sheet in route.sheets:
    % services = route.get_services(sheet)
    % trips = route.get_trips(sheet)
    % headsigns = route.get_headsigns(sheet)
    % positions = sorted(route.positions)
    
    <div id="sidebar">
        <h2>Overview</h2>
        % include('components/map', map_trips=trips, map_buses=[p.bus for p in positions])
        
        <div class="info-box">
            <div class="section">
                % include('components/services_indicator', services=services)
            </div>
            <div class="section">
                <div class="name">Headsign{{ '' if len(headsigns) == 1 else 's' }}</div>
                <div class="value">
                    % for headsign in headsigns:
                        <span>{{ headsign }}</span>
                        <br />
                    % end
                </div>
            </div>
        </div>
    </div>
    
    <div>
        % if len(positions) > 0:
            <h2>Active Buses</h2>
            <table class="pure-table pure-table-horizontal pure-table-striped">
                <thead>
                    <tr>
                        <th>Bus</th>
                        <th class="desktop-only">Model</th>
                        <th>Headsign</th>
                        <th class="desktop-only">Block</th>
                        <th>Trip</th>
                        <th class="non-mobile">Current Stop</th>
                    </tr>
                </thead>
                <tbody>
                    % for position in positions:
                        % bus = position.bus
                        % trip = position.trip
                        % stop = position.stop
                        % order = bus.order
                        <tr>
                            <td>
                                % if bus.is_unknown:
                                    {{ bus }}
                                % else:
                                    <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                % end
                                % if order is not None:
                                    <span class="non-desktop smaller-font">
                                        <br />
                                        {{ order }}
                                    </span>
                                % end
                            </td>
                            <td class="desktop-only">
                                % if order is not None:
                                    {{ order }}
                                % end
                            </td>
                            <td>{{ trip }}</td>
                            <td class="desktop-only">
                                % block = trip.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            </td>
                            <td><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
                            % if stop is None:
                                <td class="non-mobile lighter-text">Unavailable</td>
                            % else:
                                <td class="non-mobile">
                                    % include('components/adherence_indicator', adherence=position.schedule_adherence)
                                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                </td>
                            % end
                        </tr>
                    % end
                </tbody>
            </table>
        % end
        
        <h2>Today's Schedule</h2>
        
        % today_trips = [t for t in trips if t.service.is_today]
        % direction_ids = {t.direction_id for t in today_trips}
        
        % if len(today_trips) == 0:
            <p>
                There are no trips for this route today.
                You can check the <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}">full schedule</a> for more information about when this route runs.
            </p>
        % else:
            <div class="container">
                % for direction_id in direction_ids:
                    % direction_trips = [t for t in today_trips if t.direction_id == direction_id]
                    % if len(direction_trips) > 0:
                        <div class="section">
                            % if len(direction_ids) > 1:
                                % directions = sorted({t.direction for t in direction_trips})
                                <h3>{{ '/'.join(directions) }}</h3>
                            % end
                            % include('components/service_trips', trips=direction_trips)
                        </div>
                    % end
                % end
            </div>
        % end
    </div>
    
    % include('components/top_button')
% else:
    <p>
        This route is not included in the {{ sheet.value }} sheet.
    </p>
% end
