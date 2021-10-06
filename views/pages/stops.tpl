% rebase('base', title='Stops')

<div class="page-header">
    <h1 class="title">Stops</h1>
    % if search is not None:
        <h2 class="subtitle">Search results for "{{ search }}"</h2>
    % end
</div>
<hr />

% if system is None:
    <p>
        Stops can only be viewed for individual systems.
        Please choose a system.
    </p>
    % include('components/systems')
% else:
    % stops = system.all_stops()
    
    % if search is not None:
        % stops = [s for s in stops if search.lower() in s.name.lower()]
    % end
    
    % if len(stops) == 0:
        <p>No stops found</p>
    % else:
        <table class="pure-table pure-table-horizontal pure-table-striped">
            <thead>
                <tr>
                    <th class="desktop-only">Stop Number</th>
                    <th class="mobile-only">Number</th>
                    <th class="desktop-only">Stop Name</th>
                    <th class="mobile-only">Name</th>
                    <th>Routes</th>
                </tr>
            </thead>
            <tbody>
                % for stop in sorted(stops):
                    <tr>
                        <td><a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a></td>
                        <td>{{ stop }}</td>
                        <td>{{ stop.routes_string }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end
