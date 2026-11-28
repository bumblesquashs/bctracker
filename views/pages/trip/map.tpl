
% rebase('base')

<div id="page-header">
    <h1>Trip {{! trip.display_id }}</h1>
    <h2>
        % include('components/headsign')
    </h2>
    <div class="tab-button-bar">
        <a href="{{ trip.url() }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        % if config.realtime_enabled and config.enable_realtime_trips:
            <a href="{{ trip.url('history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% departures = trip.find_departures()

% include('components/map', is_preview=False, map_trip=trip, map_departures=departures, map_positions=positions)
