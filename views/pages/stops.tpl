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
    % stops = system.get_stops(sheet)
    
    % if search is not None:
        % stops = [s for s in stops if search.lower() in s.name.lower()]
    % end
    
    <script>
        function stopSearch() {
            let value = document.getElementById('stop_id_search').value;
            if (value.length > 0) {
                window.location = "{{ get_url(system) }}/stops?search=" + value;
            } else {
                window.location = "{{ get_url(system) }}/stops";
            }
        }
    </script>
    
    <form onsubmit="stopSearch()" action="javascript:void(0)">
        <label for="stop_id_search">Stop Name:</label>
        <br />
        <input type="text" id="stop_id_search" name="stop_id" method="post" value="{{ search or '' }}">
        <input type="submit" value="Search" class="button">
    </form>
    
    % if len(stops) == 0:
        <p>No stops found</p>
    % else:
        <table class="pure-table pure-table-horizontal pure-table-striped">
            <thead>
                <tr>
                    <th class="desktop-only">Stop Number</th>
                    <th class="non-desktop">Number</th>
                    <th class="desktop-only">Stop Name</th>
                    <th class="non-desktop">Name</th>
                    <th>Routes</th>
                </tr>
            </thead>
            <tbody>
                % for stop in sorted(stops):
                    <tr>
                        <td><a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a></td>
                        <td>{{ stop }}</td>
                        <td>{{ stop.get_routes_string(sheet) }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end

% include('components/top_button')
