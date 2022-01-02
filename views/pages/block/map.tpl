
% rebase('base', title=f'Block {block.id}', include_maps=True)

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

% trips = block.get_trips(sheet)
% departures = [d for t in trips for d in t.departures]
% buses = [p.bus for p in block.positions]

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_buses=buses)
