
% rebase('base')

% model = vehicle.model

<div id="page-header">
    <h1 class="row">
        % if model:
            % title_prefix = model.type.title_prefix
            % if title_prefix:
                <span>{{ title_prefix }}</span>
            % end
        % end
        % include('components/vehicle', enable_link=False)
        % include('components/favourite')
    </h1>
    % year_model = vehicle.year_model
    % if year_model:
        <h2>{{! year_model }}</h2>
    % else:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % end
    <div class="tab-button-bar">
        % if context.system:
            <a href="{{ get_url(context, 'bus', vehicle) }}" class="tab-button">Overview</a>
            <span class="tab-button current">Map</span>
            <a href="{{ get_url(context, 'bus', vehicle, 'history') }}" class="tab-button">History</a>
        % else:
            <a href="{{ get_url(context, 'bus', vehicle.agency, vehicle) }}" class="tab-button">Overview</a>
            <span class="tab-button current">Map</span>
            <a href="{{ get_url(context, 'bus', vehicle.agency, vehicle, 'history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% if position:
    % trip = position.trip
    % if trip:
        % include('components/map', is_preview=False, map_position=position, map_trip=trip, map_departures=trip.find_departures(), zoom_trips=False, zoom_departures=False)
    % else:
        % include('components/map', is_preview=False, map_position=position)
    % end
% else:
    % if last_position:
        <div class="warning-box align-start">
            % include('components/svg', name='status/warning')
            <p>Offline — showing last known location</p>
        </div>
        % include('components/map', is_preview=False, map_position=last_position, offline=True)
    % else:
        <div class="warning-box align-start">
            % include('components/svg', name='status/warning')
            <p>Offline — last known location not available</p>
        </div>
    % end
% end
