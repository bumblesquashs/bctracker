
% rebase('base')

<div class="page-header">
    <h1 class="row">
        <span>Bus</span>
        % include('components/bus', bus=bus, enable_link=False)
    </h1>
    % if bus.order is None:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % else:
        <h2>{{! bus.order }}</h2>
    % end
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(system, f'bus/{bus.number}/history') }}" class="tab-button">History</a>
    </div>
</div>

% if position is None:
    <div class="placeholder">
        <h3>Not in service</h3>
    </div>
% else:
    % trip = position.trip
    % if trip is None:
        % include('components/map', is_preview=False, map_position=position)
    % else:
        % include('components/map', is_preview=False, map_position=position, map_trip=trip, map_departures=trip.find_departures(), zoom_trips=False, zoom_departures=False)
    % end

    % include('components/map_toggle')
% end
