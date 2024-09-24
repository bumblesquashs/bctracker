
% rebase('base')

<div id="page-header">
    <h1>Stops</h1>
</div>

% if system:
    % stops = system.get_stops()
    <script>
        const routesFilter = new Set("{{ ','.join(routes_filter) }}".split(",").filter(function(route) {
            return route !== "";
        }));
        let sort = "{{ sort }}";
        let sortOrder = "{{ sort_order }}";
        
        function toggleRouteFilter(number) {
            if (routesFilter.has(number)) {
                routesFilter.delete(number);
            } else {
                routesFilter.add(number);
            }
            updateFilters();
        }
        
        function resetRoutesFilter() {
            routesFilter.clear();
            updateFilters();
        }
        
        function setSort(newSort) {
            sort = newSort;
            updateFilters();
        }
        
        function setSortOrder(newSortOrder) {
            sortOrder = newSortOrder;
            updateFilters();
        }
        
        function updateFilters() {
            const search = document.getElementById('stop_id_search').value;
            window.location = getUrl(systemID, "stops", {
                "search": search.length === 0 ? null : search,
                "routes": routesFilter.size === 0 ? null : Array.from(routesFilter).sort().join(","),
                "sort": sort === "name" ? null : sort,
                "sort_order": sortOrder === "asc" ? null : sortOrder
            })
        }
    </script>
    <div class="page-container">
        <div class="sidebar container flex-1">
            <div class="section {{ '' if search or routes_filter else 'closed' }}">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Filters</h2>
                    % include('components/toggle')
                </div>
                <div class="content gap-20">
                    <form onsubmit="updateFilters()" action="javascript:void(0)">
                        <label for="stop_id_search">Stop Name:</label>
                        <div class="input-container">
                            <input type="text" id="stop_id_search" name="stop_id" method="post" value="{{ search or '' }}" size="10">
                            <input type="submit" value="Search" class="button">
                        </div>
                    </form>
                    <div class="info-box">
                        <div class="row section">
                            <div class="lighter-text">
                                % if routes_filter:
                                    % if len(routes_filter) == 1:
                                        1 route selected
                                    % else:
                                        {{ len(routes_filter) }} routes selected
                                    % end
                                % else:
                                    No routes selected
                                % end
                            </div>
                            <button class="button compact" onclick="resetRoutesFilter()">Reset</button>
                        </div>
                        <div class="section">
                            <div class="options-container">
                                % for route in system.get_routes():
                                    <div class="option space-between" onclick="toggleRouteFilter('{{ route.number }}')">
                                        <div class="row">
                                            % include('components/route')
                                            {{! route.display_name }}
                                        </div>
                                        <div class="checkbox {{ 'selected' if route.number in routes_filter else '' }}">
                                            % include('components/svg', name='check')
                                        </div>
                                    </div>
                                % end
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="section {{ 'closed' if sort == 'name' and sort_order == 'asc' else '' }}">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Sorting</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="info-box columns">
                        <div class="section">
                            <div class="options-container">
                                <div class="option" onclick="setSort('name')">
                                    <div class="radio-button {{ 'selected' if sort == 'name' else '' }}"></div>
                                    <div>Stop Name</div>
                                </div>
                                <div class="option" onclick="setSort('number')">
                                    <div class="radio-button {{ 'selected' if sort == 'number' else '' }}"></div>
                                    <div>Stop Number</div>
                                </div>
                            </div>
                        </div>
                        <div class="section">
                            <div class="options-container">
                                <div class="option" onclick="setSortOrder('asc')">
                                    <div class="radio-button {{ 'selected' if sort_order == 'asc' else '' }}"></div>
                                    <div>Ascending</div>
                                </div>
                                <div class="option" onclick="setSortOrder('desc')">
                                    <div class="radio-button {{ 'selected' if sort_order == 'desc' else '' }}"></div>
                                    <div>Descending</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container flex-3">
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>
                        % if search:
                            Results for "{{ search }}"
                        % elif routes_filter:
                            Results
                        % else:
                            All Stops
                        % end
                    </h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if search:
                        % stops = [s for s in stops if search.lower() in s.name.lower()]
                    % end
                    % for route_number in routes_filter:
                        % stops = [s for s in stops if route_number in {r.number for r in s.routes}]
                    % end
                    % if sort == 'number':
                        % stops.sort(key=lambda s: s.number, reverse=sort_order == 'desc')
                    % elif sort == 'name':
                        % stops.sort(key=lambda s: s.name, reverse=sort_order == 'desc')
                    % end
                    % if stops:
                        <table>
                            <thead>
                                <tr>
                                    <th class="desktop-only">Stop Number</th>
                                    <th class="non-desktop">Number</th>
                                    <th class="desktop-only">Stop Name</th>
                                    <th class="non-desktop">Name</th>
                                    <th class="non-mobile">Routes</th>
                                    <th class="desktop-only">Service Days</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for stop in stops:
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
                                        <td class="desktop-only">
                                            % include('components/weekdays', schedule=stop.schedule, compact=True, schedule_path=f'stops/{stop.number}/schedule')
                                        </td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                        
                        % include('components/top_button')
                    % else:
                        <div class="placeholder">
                            % if search or routes_filter:
                                <h3>No stops found</h3>
                                % if search and routes_filter:
                                    <p>Please try a different search or selecting different routes!</p>
                                % elif search:
                                    <p>Please try a different search!</p>
                                % else:
                                    <p>Please try selecting different routes!</p>
                                % end
                            % else:
                                <h3>Stop information for {{ system }} is unavailable</h3>
                                % if system.gtfs_loaded:
                                    <p>Please check again later!</p>
                                % else:
                                    <p>System data is currently loading and will be available soon.</p>
                                % end
                            % end
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
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
