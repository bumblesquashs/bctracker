% import json

% rebase('base', title=f'Trip {trip.id} - Map', include_maps=True)

<div class="page-header map-page">
    <h1 class="title">Trip {{ trip.id }} - Map</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <a href="{{ get_url(system, f'trips/{trip.id}') }}">Return to trip overview</a>
</div>

% stops = {d.stop for d in trip.departures}
% buses = [p.bus for p in trip.positions]

% include('components/map', is_preview=False, trip=trip, stops=stops, buses=buses)
