
% rebase('base', title=str(route), include_maps=True)

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
</div>
<hr />

% direction_ids = {t.direction_id for t in route.trips}

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
            % service_trips = [t for t in route.trips if t.service == service]
            <div class="section">
                <h3 class="title" id="{{service}}">{{ service }}</h3>
                <div class="subtitle">{{ service.date_string }}</div>
                <div class="container">
                    % for direction_id in direction_ids:
                        % direction_trips = [t for t in service_trips if t.direction_id == direction_id]
                        <div class="section">
                            % if len(direction_ids) > 1:
                                % directions = sorted({t.direction for t in direction_trips})
                                <h4>{{ '/'.join(directions) }}</h4>
                            % end
                            % include('components/service_trips', trips=direction_trips)
                        </div>
                    % end
                </div>
            </div>
        % end
    </div>
</div>
