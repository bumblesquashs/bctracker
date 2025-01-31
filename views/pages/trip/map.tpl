
% rebase('base')

<div id="page-header">
    <h1>Trip {{! trip.display_id }}</h1>
    <h2>{{ trip }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'trips', trip) }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, 'trips', trip, 'history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% departures = trip.find_departures()

% include('components/map', is_preview=False, map_trip=trip, map_departures=departures, map_positions=positions)
