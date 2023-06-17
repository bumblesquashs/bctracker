
% rebase('base')

<div class="page-header">
    <h1 class="title">Error: Stop {{ stop_number }} Not Found</h1>
</div>

<p>The stop you are looking for doesn't seem to exist!</p>
<p>
    There are a few reasons why that might be the case:
    <ol>
        <li>It may no longer serve any bus routes and therefore be removed from the system</li>
        <li>It may be the wrong number - are you sure stop {{ stop_number }} is the one you want?</li>
        % alt_systems = [s for s in systems if s.get_stop(number=stop_number) is not None]
        % if len(alt_systems) > 0:
            <li>
                It may be from a different system - the following systems have a stop with that number
                <ul>
                    % for alt_system in alt_systems:
                        <li>{{ alt_system }}: <a href="{{ get_url(alt_system, f'stops/{stop_number}') }}">{{ alt_system.get_stop(number=stop_number) }}</a></li>
                    % end
                </ul>
            </li>
        % end
        <li>It may be from a system that isn't currently available on BC Tracker</li>
    </ol>
</p>

<p>
    If you believe this error is incorrect and the stop actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!
</p>

<p>
    <button class="button" onclick="window.history.back()">Back</button>
</p>
