
% rebase('base', title=f'Bus {bus}', include_maps=True, full_map=True)

% if position is None:
    <div class="page-header">
        <h1 class="title">Bus {{ bus }}</h1>
        <h2 class="subtitle">
            % if bus.order is None:
                <span class="lighter-text">Unknown Year/Model</span>
            % else:
                {{! bus.order }}
            % end
        </h2>
        <div class="tab-button-bar">
            <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
            <span class="tab-button current">Map</span>
            <a href="{{ get_url(system, f'bus/{bus.number}/history') }}" class="tab-button">History</a>
        </div>
        <hr />
    </div>
    
    <h3>Not in service</h3>
% else:
    <div class="page-header map-page">
        <h1 class="title">Bus {{ bus }}</h1>
        <h2 class="subtitle">
            % if bus.order is None:
                Unknown Year/Model
            % else:
                {{! bus.order }}
            % end
        </h2>
        <div class="tab-button-bar">
            <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
            <span class="tab-button current">Map</span>
            <a href="{{ get_url(system, f'bus/{bus.number}/history') }}" class="tab-button">History</a>
        </div>
    </div>
    
    % trip = position.trip
    % if trip is None:
        % include('components/map', is_preview=False, map_position=position)
    % else:
        % include('components/map', is_preview=False, map_position=position, map_trip=trip, map_departures=trip.departures, zoom_trips=False, zoom_departures=False)
    % end

    % include('components/map_toggle')
% end
