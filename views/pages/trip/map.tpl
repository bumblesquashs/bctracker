
% rebase('base', title=f'Trip {trip.id}', include_maps=True, show_refresh_button=True)

<div class="page-header map-page">
    <h1 class="title trip-id">Trip {{ trip.id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'trips/{trip.id}') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Map</span>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'trips/{trip.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% departures = trip.departures

% include('components/map', is_preview=False, map_trip=trip, map_departures=departures, map_positions=positions)

% include('components/map_z_toggle')
