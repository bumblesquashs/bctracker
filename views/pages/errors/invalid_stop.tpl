
% rebase('base')

<div id="page-header">
    <h1>Error: Stop {{ stop_number }} Not Found</h1>
</div>

<div class="placeholder">
    <h3>The stop you are looking for doesn't seem to exist!</h3>
    % if context.gtfs_loaded:
        <p>There are a few reasons why that might be the case:</p>
        <ol>
            <li>It may no longer serve any bus routes and therefore be removed from the system</li>
            <li>It may be the wrong number - are you sure stop <b>{{ stop_number }}</b> is the one you want?</li>
            % alt_stops = [s.get_stop(number=stop_number) for s in systems if s.get_stop(number=stop_number)]
            % if alt_stops:
                <li>
                    It may be from a different system - the following systems have a stop with that number
                    <ul>
                        % for stop in alt_stops:
                            <li>
                                {{ stop.context }}:
                                % include('components/stop', show_number=False)
                            </li>
                        % end
                    </ul>
                </li>
            % end
            <li>It may be from a system that isn't currently available on BC Tracker</li>
        </ol>
        <p>If you believe this error is incorrect and the stop actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!</p>
        
        <button class="button" onclick="window.history.back()">Back</button>
    % else:
        <p>System data is currently loading and will be available soon.</p>
    % end
</div>
