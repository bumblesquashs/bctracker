
% rebase('base', title=f'Trip {trip.id}', include_maps=True)

<div class="page-header map-page">
    <h1 class="title">Trip {{ trip.id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'trips/{trip.id}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
    </div>
</div>

% departures = trip.departures
% buses = [p.bus for p in trip.positions]

% include('components/map', is_preview=False, map_trip=trip, map_departures=departures, map_buses=buses)
