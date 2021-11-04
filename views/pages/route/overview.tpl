
% rebase('base', title=str(route), include_maps=True)

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
</div>
<hr />

% if sheet is None or sheet in route.sheets:
    % services = route.get_services(sheet)
    % trips = route.get_trips(sheet)
    % headsigns = route.get_headsigns(sheet)

    % direction_ids = {t.direction_id for t in trips}

    <div id="sidebar">
        <h2>Overview</h2>
        % include('components/route_map', route=route)
        
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
        % positions = route.positions
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
                                <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
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
        
        <h2>Trip Schedule</h2>
        <div class="container">
            % if len(services) > 1:
                <div class="navigation">
                    % for service in services:
                        <a href="#{{service}}" class='button'>{{ service }}</a>
                    % end
                </div>
                <br />
            % end
            
            % for service in services:
                % service_trips = [t for t in trips if t.service == service]
                <div class="section">
                    <h3 class="title" id="{{service}}">{{ service }}</h3>
                    <div class="subtitle">{{ service.date_string }}</div>
                    <div class="container">
                        % for direction_id in direction_ids:
                            % direction_trips = [t for t in service_trips if t.direction_id == direction_id]
                            % if len(direction_trips) > 0:
                                <div class="section">
                                    % if len(direction_ids) > 1:
                                        % directions = sorted({t.direction for t in direction_trips})
                                        <h4>{{ '/'.join(directions) }}</h4>
                                    % end
                                    % include('components/service_trips', trips=direction_trips)
                                </div>
                            % end
                        % end
                    </div>
                </div>
            % end
        </div>
    </div>
    
    % include('components/top_button')
% else:
    <p>
        This route is not included in the {{ sheet.value }} sheet.
    </p>
% end
