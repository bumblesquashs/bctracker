
% rebase('base', title=f'Block {block.id}', include_maps=True, full_map=True, show_refresh_button=True)

<div class="page-header map-page">
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
% departures = [d for t in trips for d in t.departures]

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_positions=positions)

% include('components/map_z_toggle')
