
% rebase('base')

<div id="page-header">
    <h1>Stops</h1>
    % if search:
        <h2>Search results for "{{ search }}"</h2>
    % end
</div>

% if system:
    % stops = system.get_stops()
    % if stops or search:
        % if search:
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
            <div class="input-container">
                <input type="text" id="stop_id_search" name="stop_id" method="post" value="{{ search or '' }}" size="10">
                <input type="submit" value="Search" class="button">
            </div>
        </form>
        
        % if stops:
            <table>
                <thead>
                    <tr>
                        <th class="desktop-only">Stop Number</th>
                        <th class="non-desktop">Number</th>
                        <th class="desktop-only">Stop Name</th>
                        <th class="non-desktop">Name</th>
                        <th class="non-mobile">Routes</th>
                    </tr>
                </thead>
                <tbody>
                    % for stop in sorted(stops):
                        <tr>
                            <td><a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a></td>
                            <td>
                                {{ stop }}
                                <div class="mobile-only">
                                    % include('components/route_list', routes=stop.routes)
                                </div>
                            </td>
                            <td class="non-mobile">
                                % include('components/route_list', routes=stop.routes)
                            </td>
                        </tr>
                    % end
                </tbody>
            </table>
        % else:
            <div class="placeholder">
                <h3>No stops found</h3>
            </div>
        % end

        % include('components/top_button')
    % else:
        <div class="placeholder">
            <h3>Stop information for {{ system }} is unavailable</h3>
            % if system.gtfs_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        </div>
    % end
% else:
    <div class="placeholder">
        <p>Choose a system to see individual stops.</p>
        <table>
            <thead>
                <tr>
                    <th>System</th>
                    <th class="non-mobile align-right">Stops</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if region_systems:
                        <tr class="header">
                            <td colspan="3">
                                {{ region }}
                            </td>
                        </tr>
                        <tr class="display-none"></tr>
                        % for region_system in sorted(region_systems):
                            % count = len(region_system.get_stops())
                            <tr>
                                <td>
                                    <div class="column">
                                        <a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
                                        <span class="mobile-only smaller-font">
                                            % if region_system.gtfs_loaded:
                                                % if count == 1:
                                                    1 Stop
                                                % else:
                                                    {{ count }} Stops
                                                % end
                                            % end
                                        </span>
                                    </div>
                                </td>
                                % if region_system.gtfs_loaded:
                                    <td class="non-mobile align-right">{{ count }}</td>
                                    <td>
                                        % include('components/weekdays', schedule=region_system.schedule, compact=True)
                                    </td>
                                % else:
                                    <td class="lighter-text" colspan="2">Stops are loading...</td>
                                % end
                            </tr>
                        % end
                    % end
                % end
            </tbody>
        </table>
    </div>
% end
