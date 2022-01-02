
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

% if sheet is None or sheet in route.sheets:
    % services = route.get_services(sheet)
    % trips = route.get_trips(sheet)
    
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
            % direction_ids = {t.direction_id for t in service_trips}
            <div class="section">
                <h2 class="title" id="{{service}}">{{ service }}</h2>
                <div class="subtitle">{{ service.date_string }}</div>
                <div class="container">
                    % for direction_id in direction_ids:
                        % direction_trips = [t for t in service_trips if t.direction_id == direction_id]
                        <div class="section">
                            % if len(direction_ids) > 1:
                                % directions = sorted({t.direction for t in direction_trips})
                                <h3>{{ '/'.join(directions) }}</h3>
                            % end
                            % include('components/service_trips', trips=direction_trips)
                        </div>
                    % end
                </div>
            </div>
        % end
    </div>
    
    % include('components/top_button')
% else:
    <p>This route is not included in the {{ sheet.value }} sheet.</p>
% end