% from models.trip import Direction

% rebase('base', title=str(route), include_maps=True)

<h1>{{ route }}</h1>
<hr />

% services = route.get_services(None)
% trips = route.get_trips(None)
% headsigns = route.get_headsigns(None)

% outbound_trips = [t for t in trips if t.direction == Direction.OUTBOUND]
% inbound_trips = [t for t in trips if t.direction == Direction.INBOUND]

% has_outbound_trips = len(outbound_trips) > 0
% has_inbound_trips = len(inbound_trips) > 0

<div id="sidebar">
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
        % service_outbound_trips = [t for t in outbound_trips if t.service == service]
        % service_inbound_trips = [t for t in inbound_trips if t.service == service]
        <div class="section">
            <h2 class="title" id="{{service}}">{{ service }}</h2>
            <div class="subtitle">{{ service.date_string }}</div>
            <div class="container">
                % if len(inbound_trips) > 0:
                    <div class="section">
                        % if len(service_outbound_trips) > 0:
                            <h3>Inbound</h3>
                        % end
                        % include('components/service_trips', trips=service_inbound_trips)
                    </div>
                % end
                
                % if len(service_outbound_trips) > 0:
                    <div class="section">
                        % if len(service_inbound_trips) > 0:
                            <h3>Outbound</h3>
                        % end
                        % include('components/service_trips', trips=service_outbound_trips)
                    </div>
                % end
            </div>
        </div>
    % end
</div>
