
% rebase('base')

<div id="page-header">
    <h1>Error: Route {{ route_number }} Not Found</h1>
</div>

<div class="placeholder">
    <h3>The route you are looking for doesn't seem to exist!</h3>
    % if context.gtfs_loaded:
        <p>There are a few reasons why that might be the case:</p>
        <ol>
            <li>It may be from an older sheet that is no longer active</li>
            <li>It may be the wrong number - are you sure route <b>{{ route_number }}</b> is the one you want?</li>
            % alt_routes = [s.get_route(number=route_number) for s in systems if s.get_route(number=route_number)]
            % if alt_routes:
                <li>
                    It may be from a different system - the following systems have a route with that number
                    <ul>
                        % for route in alt_routes:
                            <li>{{ route.context }}: <a href="{{ get_url(route.context, 'routes', route) }}">{{ route }}</a></li>
                        % end
                    </ul>
                </li>
            % end
            <li>It may be from a system that isn't currently available on BC Tracker</li>
            <li>It may be an on-request service that isn't included in the normal schedule</li>
        </ol>
        <p>If you believe this error is incorrect and the route actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!</p>
        
        <button class="button" onclick="window.history.back()">Back</button>
    % else:
        <p>System data is currently loading and will be available soon.</p>
    % end
</div>
