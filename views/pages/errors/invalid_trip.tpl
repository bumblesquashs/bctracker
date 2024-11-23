
% rebase('base')

<div id="page-header">
    <h1>Error: Trip {{ trip_id }} Not Found</h1>
</div>

<div class="placeholder">
    <h3>The trip you are looking for doesn't seem to exist!</h3>
    % if system.gtfs_loaded:
        <p>There are a few reasons why that might be the case:</p>
        <ol>
            <li>It may be from an older sheet that is no longer active</li>
            <li>It may be the wrong ID - are you sure trip <b>{{ trip_id }}</b> is the one you want?</li>
            % alt_trips = [s.get_trip(trip_id) for s in systems if s.get_trip(trip_id)]
            % if alt_trips:
                <li>
                    It may be from a different system - the following systems have a trip with that ID
                    <ul>
                        % for trip in alt_trips:
                            <li>{{ trip.system }}: <a href="{{ get_url(trip.system, 'trips', trip) }}">Trip {{ trip }}</a></li>
                        % end
                    </ul>
                </li>
            % end
        </ol>
        <p>If you believe this error is incorrect and the trip actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!</p>
        
        <button class="button" onclick="window.history.back()">Back</button>
    % else:
        <p>System data is currently loading and will be available soon.</p>
    % end
</div>
