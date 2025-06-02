
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/stop', include_link=False)
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'stops', stop) }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(context, 'stops', stop, 'schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

% trips = [d.trip for d in stop.departures if d.trip and d.trip.route]

% include('components/map', is_preview=False, map_trips=trips, map_departures=adjacent_departures, map_stop=stop, zoom_trips=False, zoom_departures=False)
