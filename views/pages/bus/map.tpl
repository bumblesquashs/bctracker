
% rebase('base', title=f'Bus {bus}', include_maps=True)

% position = bus.position
% if not position.active:
    <div class="page-header">
        <h1 class="title">Bus {{ bus }}</h1>
        <h2 class="subtitle">{{ bus.order }}</h2>
        <div class="tab-button-bar">
            <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
            <span class="tab-button current">Map</span>
            <a href="{{ get_url(system, f'bus/{bus.number}/history') }}" class="tab-button">History</a>
        </div>
    </div>
    <hr />
    
    <h3>Not in service</h3>
% else:
    <div class="page-header map-page">
        <h1 class="title">Bus {{ bus }}</h1>
        <h2 class="subtitle">{{ bus.order }}</h2>
        <div class="tab-button-bar">
            <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
            <span class="tab-button current">Map</span>
            <a href="{{ get_url(system, f'bus/{bus.number}/history') }}" class="tab-button">History</a>
        </div>
    </div>
    
    % if position.trip is None:
        % include('components/map', is_preview=False, map_bus=bus)
    % else:
        % trip = position.trip
        % include('components/map', is_preview=False, map_bus=bus, map_trip=trip, map_departures=trip.departures, zoom_trips=False, zoom_departures=False)
    % end
% end
