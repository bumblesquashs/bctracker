
% rebase('base', title=f'Block {block.id} - Map', include_maps=True)

<div class="page-header map-page">
    <h1 class="title">Block {{ block.id }} - Map</h1>
    <a href="{{ get_url(system, f'blocks/{block.id}') }}">Return to block overview</a>
</div>

% trips = block.get_trips(sheet)
% departures = [d for t in trips for d in t.departures]
% buses = [p.bus for p in block.positions]

% include('components/map', is_preview=False, trips=trips, departures=departures, buses=buses)
