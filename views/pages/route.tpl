% from models.trip import Direction

% rebase('base', title=str(route), include_maps=True)

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
</div>
<hr />

% outbound_trips = [t for t in route.trips if t.direction == Direction.OUTBOUND]
% inbound_trips = [t for t in route.trips if t.direction == Direction.INBOUND]

% has_outbound_trips = len(outbound_trips) > 0
% has_inbound_trips = len(inbound_trips) > 0

<div id="sidebar">
    <h2>Overview</h2>
    % include('components/route_map', route=route)
    
    <div class="info-box">
        <div class="section">
            % include('components/services_indicator', services=route.services)
        </div>
        <div class="section">
            <div class="name">Headsign{{ '' if len(route.headsigns) == 1 else 's' }}</div>
            <div class="value">
                % for headsign in route.headsigns:
                    <span>{{ headsign }}</span>
                    <br />
                % end
            </div>
        </div>
    </div>
</div>

<div>
    <h2>Trip Schedule</h2>
    <div class="container">
        % if len(route.services) > 1:
            <div class="navigation">
                % for service in route.services:
                    <a href="#{{service}}" class='button'>{{ service }}</a>
                % end
            </div>
            <br />
        % end
        
        % for service in route.services:
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
</div>
