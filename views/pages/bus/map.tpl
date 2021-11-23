
% rebase('base', title=f'Bus {{ bus }} - Map', include_maps=True)

% position = bus.position
% if not position.active:
    <div class="page-header">
        <h1 class="title">Bus {{ bus }} - Map</h1>
        <h2 class="subtitle">{{ bus.order }}</h2>
        <a href="{{ get_url(system, f'bus/{bus.number}') }}">Return to bus overview</a>
    </div>
    <hr />
    
    <h3>Not in service</h3>
% else:
    <div class="page-header map-page">
        <h1 class="title">Bus {{ bus }} - Map</h1>
        <h2 class="subtitle">{{ bus.order }}</h2>
        <a href="{{ get_url(system, f'bus/{bus.number}') }}">Return to bus overview</a>
    </div>
    
    % if position.trip is None:
        % include('components/map', is_preview=False, bus=bus)
    % else:
        % trip = position.trip
        % include('components/map', is_preview=False, bus=bus, trip=trip, departures=trip.departures)
    % end
% end
