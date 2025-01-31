
% rebase('base')

<div id="page-header">
    <h1 class="row">
        <span>Bus</span>
        % include('components/bus', enable_link=False)
        % include('components/favourite')
    </h1>
    % if bus.order:
        <h2>{{! bus.order }}</h2>
    % else:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % end
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'bus', bus) }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(system, 'bus', bus, 'history') }}" class="tab-button">History</a>
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
        <h3>Not in service</h3>
    </div>
% end
