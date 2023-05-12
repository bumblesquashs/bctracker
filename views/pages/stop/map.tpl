
% import helpers.departure

% rebase('base', title=f'Stop {stop.number}', include_maps=True, full_map=True)

<div class="page-header map-page">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'stops/{stop.number}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

% trips = [d.trip for d in stop.get_departures()]
% departures = helpers.departure.find_all(stop.system.id, trip_id=[t.id for t in trips])

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_stop=stop, zoom_trips=False, zoom_departures=False)

% include('components/map_toggle')
