
% rebase('base')

<div class="page-header">
    <h1 class="title">
        <div class="flex-row">
            % include('components/route_indicator')
            <div class="flex-1">{{! route.display_name }}</div>
        </div>
    </h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

% if len(route.trips) == 0:
    <div class="placeholder">
        % if system.is_loaded:
            <h3 class="title">There are currently no trips for this route</h3>
            <p>There are a few reasons why that may be the case:</p>
            <ol>
                <li>It may be an old route that is no longer in service</li>
                <li>It may be a new route that hasn't started service yet</li>
                <li>It may be used as an internal route in the GTFS that does not run any trips</li>
            </ol>
            <p>Please check again later!</p>
        % else:
            <h3 class="title">Trips for this route are unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % end
    </div>
% else:
    % trips = route.trips
    % departures = [d for t in trips for d in t.departures]
    
    % include('components/map', is_preview=False, map_trips=trips, map_departures=departures, map_positions=positions)

    % include('components/map_toggle')
% end
