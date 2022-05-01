
% rebase('base', title=str(route), include_maps=True, show_refresh_button=True)

% if len(route.trips) == 0:
    <div class="page-header">
        <h1 class="title">{{ route }}</h1>
        <div class="tab-button-bar">
            <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
            <span class="tab-button current">Map</span>
            <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
        </div>
        <hr />
    </div>
    
    <p>There are currently no trips for this route.</p>
    <p>
        There are a few reasons why that may be the case:
        <ol>
            <li>It may be an old route that is no longer in service</li>
            <li>It may be a new route that hasn't started service yet</li>
            <li>It may be used as an internal route in the GTFS that does not run any trips</li>
        </ol>
        Please check again later!
    </p>
% else:
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
% end
