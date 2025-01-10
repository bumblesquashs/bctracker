
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/route')
        <span>{{! route.display_name }}</span>
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'routes', route) }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(system, 'routes', route, 'schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

% if route.trips:
    % trips = route.trips
    % departures = route.find_departures()
    
    % include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_positions=positions)

    % include('components/map_toggle')
% else:
    <div class="placeholder">
        % if system.gtfs_loaded:
            <h3>There are currently no trips for this route</h3>
            <p>There are a few reasons why that may be the case:</p>
            <ol>
                <li>It may be an old route that is no longer in service</li>
                <li>It may be a new route that hasn't started service yet</li>
                <li>It may be used as an internal route in the GTFS that does not run any trips</li>
            </ol>
            <p>Please check again later!</p>
        % else:
            <h3>Trips for this route are unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % end
    </div>
% end
