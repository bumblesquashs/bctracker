
% rebase('base', title=str(route), include_maps=True)

<div class="page-header map-page">
    <h1 class="title">{{ route }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
    </div>
</div>

% trips = route.get_trips(sheet)
% departures = [d for t in trips for d in t.departures]
% buses = [p.bus for p in route.positions]

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_buses=buses)
