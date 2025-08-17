
% rebase('base')

<div id="page-header">
    <h1 class="row">
        <span>Bus</span>
        % include('components/bus', enable_link=False)
        % include('components/favourite')
    </h1>
    % year_model = bus.year_model
    % if year_model:
        <h2>{{! year_model }}</h2>
    % else:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % end
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'bus', bus) }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(context, 'bus', bus, 'history') }}" class="tab-button">History</a>
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
    <div class="placeholder">
        <h3>Not In Service</h3>
    </div>
    % if last_position:
        <div class="warning-box">
            % include('components/svg', name='status/warning')
            <p>Showing last known location, may not be current</p>
        </div>
        % include('components/map', is_preview=False, map_position=last_position, outdated=True)
    % end
% end
