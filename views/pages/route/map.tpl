
% rebase('base', title=f'{route} - Map', include_maps=True)

<div class="page-header map-page">
    <h1 class="title">{{ route }} - Map</h1>
    <a href="{{ get_url(system, f'routes/{route.number}') }}">Return to route overview</a>
</div>

% trips = route.get_trips(sheet)
% departures = [d for t in trips for d in t.departures]
% buses = [p.bus for p in route.positions]

% include('components/map', is_preview=False, trips=trips, departures=departures, buses=buses)
