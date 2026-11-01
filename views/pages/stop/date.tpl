
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/stop', include_link=False)
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <a href="{{ stop.url(routes=routes_query) }}" class="tab-button">Overview</a>
        <a href="{{ stop.url('map', routes=routes_query) }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Overview</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="row section align-center">
                        % previous_date = date.previous()
                        % next_date = date.next()
                        <a class="icon button" href="{{ stop.url('schedule', previous_date, routes=routes_query) }}">
                            % include('components/svg', name='paging/left')
                        </a>
                        <div class="centred">
                            <h3>{{ date.format_long() }}</h3>
                            <a href="{{ stop.url('schedule', routes=routes_query) }}">Return to week view</a>
                        </div>
                        <a class="icon button" href="{{ stop.url('schedule', next_date, routes=routes_query) }}">
                            % include('components/svg', name='paging/right')
                        </a>
                    </div>
                    <div class="section">
                        % include('components/sheet_list', sheets=stop.sheets, schedule_path=f'stops/{stop.url_id}/schedule', schedule_path_args={'routes': routes_query})
                    </div>
                    <div class="section">
                        <div class="options-container">
                            <div class="option" onclick="toggleCompactSchedule()">
                                <div class="checkbox {{ 'selected' if compact_schedule else '' }}">
                                    % include('components/svg', name='status/check')
                                </div>
                                <div>Show Compact Schedule</div>
                            </div>
                            <script>
                                function toggleCompactSchedule() {
                                    storeCurrentScrollPosition();
                                    window.location = "{{! stop.url('schedule', date.format_db(), compact_schedule='false' if compact_schedule else 'true', routes=routes_query) }}";
                                }
                            </script>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        % if len(stop.routes) > 1:
            <div class="section {{ '' if routes_filter else 'closed' }}">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Routes</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if show_help_text:
                        <p>Select routes to filter schedule.</p>
                    % end
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
                                % for route in stop.routes:
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
                <script>
                    const routesFilter = new Set("{{ ','.join(routes_filter) }}".split(",").filter(function(route) {
                        return route !== "";
                    }));
                    
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
                    
                    function updateFilters() {
                        storeCurrentScrollPosition();
                        window.location = getURL(currentAgencyID, currentSystemID, "stops/{{ stop.url_id }}/schedule/{{ date.format_db() }}", {
                            "routes": routesFilter.size === 0 ? null : Array.from(routesFilter).sort().join(","),
                        });
                    }
                </script>
            </div>
        % end
    </div>
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <div class="column">
                    <h2>{{ date.format_long() }}</h2>
                    <p>{{ date.weekday }}</p>
                </div>
                % include('components/toggle')
            </div>
            <div class="content">
                % departures = stop.find_departures(date=date)
                % if routes_filter:
                    % departures = [d for d in departures if d.trip and d.trip.route and d.trip.route.url_id in routes_filter]
                % end
                % if departures:
                    % if compact_schedule:
                        % if show_help_text and any([1 for d in departures if d.trip and d.trip.last_departure == d or not d.pickup_type.is_normal]):
                            <p>Departures with a <span class="lighter-text strike-through">line through</span> do not pick up.</p>
                        % end
                        % include('components/departure_board')
                    % else:
                        <table>
                            <thead>
                                <tr>
                                    <th>Time</th>
                                    <th class="non-mobile">Headsign</th>
                                    % if context.enable_blocks:
                                        <th class="non-mobile">Block</th>
                                    % end
                                    <th>Trip</th>
                                </tr>
                            </thead>
                            <tbody>
                                % last_time = None
                                % for departure in departures:
                                    % trip = departure.trip
                                    % block = trip.block
                                    % if not last_time:
                                        % last_time = departure.time
                                    % end
                                    <tr class="{{'divider' if departure.time.hour > last_time.hour else ''}}">
                                        <td>{{ departure.time.format_web(time_format) }}</td>
                                        <td class="non-mobile">
                                            <div class="column">
                                                % include('components/headsign')
                                                % if not departure.pickup_type.is_normal:
                                                    <span class="smaller-font italics">{{ departure.pickup_type }}</span>
                                                % elif departure == trip.last_departure:
                                                    <span class="smaller-font italics">No pick up</span>
                                                % end
                                                % if not departure.dropoff_type.is_normal:
                                                    <span class="smaller-font italics">{{ departure.dropoff_type }}</span>
                                                % end
                                            </div>
                                        </td>
                                        % if context.enable_blocks:
                                            <td class="non-mobile">
                                                % if block:
                                                    <a href="{{ block.url() }}">{{ block.id }}</a>
                                                % else:
                                                    <div class="lighter-text">Unknown</div>
                                                % end
                                            </td>
                                        % end
                                        <td>
                                            <div class="column">
                                                % include('components/trip')
                                                <span class="mobile-only smaller-font">
                                                    % include('components/headsign')
                                                </span>
                                                % if not departure.pickup_type.is_normal:
                                                    <span class="mobile-only smaller-font italics">{{ departure.pickup_type }}</span>
                                                % elif departure == trip.last_departure:
                                                    <span class="mobile-only smaller-font italics">No pick up</span>
                                                % end
                                                % if not departure.dropoff_type.is_normal:
                                                    <span class="mobile-only smaller-font italics">{{ departure.dropoff_type }}</span>
                                                % end
                                            </div>
                                        </td>
                                    </tr>
                                    % last_time = departure.time
                                % end
                            </tbody>
                        </table>
                    % end
                % else:
                    <div class="placeholder">
                        % if context.gtfs_loaded:
                            <h3>No departures found on {{ date.format_long() }}</h3>
                            <p>There are a few reasons why that might be the case:</p>
                            <ol>
                                <li>It may be a day of the week that does not normally have service</li>
                                <li>It may be a holiday in which all regular service is suspended</li>
                                <li>It may be outside of the date range for which schedules are currently available</li>
                                % if routes_filter:
                                    <li>The current routes filter may be hiding service</li>
                                % end
                            </ol>
                            <p>Please check again later!</p>
                        % else:
                            <h3>Departures for this stop are unavailable</h3>
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>
