
% rebase('base', title=str(route), include_maps=True)

<div class="page-header map-page">
    <h1 class="title">{{ route }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

% trips = route.trips
% departures = [d for t in trips for d in t.departures]

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_positions=positions)
