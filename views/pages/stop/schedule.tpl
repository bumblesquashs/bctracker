
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

% if stop.find_departures():
    % sheets = stop.sheets
    <div class="page-container">
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Overview</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section">
                            % include('components/sheet_list', schedule_path=f'stops/{stop.url_id}/schedule', schedule_path_args={'routes': routes_query})
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
                                        window.location = "{{! stop.url('schedule', compact_schedule='false' if compact_schedule else 'true', routes=routes_query) }}";
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
                            window.location = getURL(currentAgencyID, currentSystemID, "stops/{{ stop.url_id }}/schedule", {
                                "routes": routesFilter.size === 0 ? null : Array.from(routesFilter).sort().join(","),
                            });
                        }
                    </script>
                </div>
            % end
        </div>
        <div class="container flex-3">
            % for (i, sheet) in enumerate(sheets):
                % if not sheet.normal_service_groups:
                    % continue
                % end
                % path_suffix = '' if i == 0 else str(i + 1)
                <div class="section">
                    <div class="header" onclick="toggleSection(this)">
                        <h2>{{ sheet }}</h2>
                        % include('components/toggle')
                    </div>
                    <div class="content">
                        <div class="container inline">
                            % for service_group in sheet.normal_service_groups:
                                % departures = stop.find_departures(service_group)
                                % if routes_filter:
                                    % departures = [d for d in departures if d.trip and d.trip.route and d.trip.route.url_id in routes_filter]
                                % end
                                <div class="section">
                                    <div class="header" onclick="toggleSection(this)">
                                        <div>
                                            % for weekday in service_group.schedule.weekdays:
                                                <div id="{{ weekday.short_name }}{{path_suffix}}"></div>
                                            % end
                                            <h3>{{ service_group }}</h3>
                                        </div>
                                        % include('components/toggle')
                                    </div>
                                    <div class="content">
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
                                    </div>
                                </div>
                            % end
                        </div>
                    </div>
                </div>
            % end
        </div>
    </div>
    
    % include('components/top_button')
% else:
    <div class="placeholder">
        % if stop.context.gtfs_loaded:
            <h3>There are currently no departures from this stop</h3>
            <p>There are a few reasons why that may be the case:</p>
            <ol>
                <li>It may be an old stop that used to serve routes but is no longer used</li>
                <li>It may be a new stop that will soon serve routes that haven't started yet</li>
                <li>It may be used as an internal reference point in the GTFS that does not serve any routes</li>
            </ol>
            <p>Please check again later!</p>
        % else:
            <h3>Departures for this stop are unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % end
    </div>
% end
