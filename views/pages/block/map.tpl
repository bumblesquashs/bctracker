
% rebase('base')

<div id="page-header">
    <h1>Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'blocks', block) }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, 'blocks', block, 'history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% trips = block.trips
% departures = block.find_departures()

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_positions=positions)
