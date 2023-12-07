
% import helpers.departure

% rebase('base')

<div class="page-header">
    <h1 class="title">Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'blocks/{block.id}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'blocks/{block.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% trips = block.trips
% departures = helpers.departure.find_all(block.system.id, block_id=block.id)

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_positions=positions)

% include('components/map_toggle')
