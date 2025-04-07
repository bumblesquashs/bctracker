
% rebase('base')

<div id="page-header">
    <h1>Stops</h1>
</div>

% if system:
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
            window.location = getUrl(currentSystemID, "stops", true, {
                "search": search.length === 0 ? null : search,
                "routes": routesFilter.size === 0 ? null : Array.from(routesFilter).sort().join(","),
                "sort": sort === "name" ? null : sort,
                "sort_order": sortOrder === "asc" ? null : sortOrder
            })
        }
    </script>
    <div class="page-container">
        <div class="sidebar container flex-1">
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
                                % if agency.show_stop_number:
                                    <div class="option" onclick="setSort('number')">
                                        <div class="radio-button {{ 'selected' if sort == 'number' else '' }}"></div>
                                        <div>Stop Number</div>
                                    </div>
                                % end
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
                                    <div class="option space-between" onclick="toggleRouteFilter('{{ route.url_id }}')">
                                        <div class="row">
                                            % include('components/route')
                                            {{! route.display_name }}
                                        </div>
                                        <div class="checkbox {{ 'selected' if route.url_id in routes_filter else '' }}">
                                            % include('components/svg', name='status/check')
                                        </div>
                                    </div>
                                % end
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
                    % if total_items == 0:
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
                                <h3>{{ system }} stop information is unavailable</h3>
                                % if system.gtfs_loaded:
                                    <p>Please check again later!</p>
                                % else:
                                    <p>System data is currently loading and will be available soon.</p>
                                % end
                            % end
                        </div>
                    % elif stops:
                        % paging_args = dict(path_args)
                        % if routes_filter:
                            % paging_args['routes'] = ','.join(sorted(routes_filter))
                        % end
                        % include('components/paging', use_path=True, path_args=paging_args)
                        <table>
                            <thead>
                                <tr>
                                    <th>Stop</th>
                                    <th class="non-mobile">Routes</th>
                                    <th>Service Days</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for stop in stops:
                                    <tr>
                                        <td>
                                            <div class="column">
                                                % include('components/stop')
                                                <div class="mobile-only">
                                                    % include('components/route_list', routes=stop.routes)
                                                </div>
                                            </div>
                                        </td>
                                        <td class="non-mobile">
                                            % include('components/route_list', routes=stop.routes)
                                        </td>
                                        <td>
                                            % include('components/weekdays', schedule=stop.schedule, compact=True, schedule_path=f'stops/{stop.url_id}/schedule')
                                        </td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                        % include('components/paging', use_path=True, path_args=paging_args)
                        
                        % include('components/top_button')
                    % else:
                        <div class="placeholder">
                            % if page == 0:
                                <h3>Page {{ page }} does not exist...?</h3>
                                <p>If you're a software developer you may be thinking right now, "Hey, wait a minute, why doesn't this list start at 0?!‽"</p>
                                <p>
                                    Look, we agree with you, it feels weird to be showing this error message at all.
                                    Sadly too many people are expecting page 1 to be the first because "it makes more sense" or "0 isn't a real number" or something equally silly.
                                    But you should know that we're right and they're just mad about it.
                                </p>
                                <p>Unfortunately you do still need to return to a <a href="?page=1">valid page</a> but remember that one day the zero-based indexers shall rise up and claim our rightful place once and for all!</p>
                            % else:
                                <h3>Page {{ page }} does not exist!</h3>
                                <p>If you got to this page through <i>nefarious tomfoolery</i> or <i>skullduggery</i>, please return to a <a href="?page=1">valid page</a>, then go sit in a corner and think about what you've done.</p>
                                <p>
                                    If you got to this page by accident, we're very sorry.
                                    Please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!
                                </p>
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
                                    <div class="row">
                                        % include('components/agency_logo', agency=region_system.agency)
                                        <div class="column">
                                            <a href="{{ get_url(region_system, *path) }}">{{ region_system }}</a>
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
