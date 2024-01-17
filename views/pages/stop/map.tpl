
% rebase('base')

<div class="page-header">
    <h1>Stop {{ stop.number }}</h1>
    <h2>{{ stop }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'stops/{stop.number}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

% trips = [d.trip for d in stop.find_departures() if d.trip is not None and d.trip.route is not None]
% departures = stop.find_adjacent_departures()

% include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_stop=stop, zoom_trips=False, zoom_departures=False)

% include('components/map_toggle')
