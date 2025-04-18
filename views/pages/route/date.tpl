
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/route')
        <span>{{! route.display_name }}</span>
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'routes', route) }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, 'routes', route, 'map') }}" class="tab-button">Map</a>
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
                        <a class="icon button" href="{{ get_url(system, 'routes', route, 'schedule', previous_date) }}">
                            % include('components/svg', name='paging/left')
                        </a>
                        <div class="centred">
                            <h3>{{ date.format_long() }}</h3>
                            <a href="{{ get_url(system, 'routes', route, 'schedule') }}">Return to week view</a>
                        </div>
                        <a class="icon button" href="{{ get_url(system, 'routes', route, 'schedule', next_date) }}">
                            % include('components/svg', name='paging/right')
                        </a>
                    </div>
                    <div class="section">
                        % include('components/sheet_list', sheets=route.sheets, schedule_path=f'routes/{route.url_id}/schedule')
                    </div>
                </div>
            </div>
        </div>
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
                % trips = route.get_trips(date=date)
                % if trips:
                    <div class="container inline">
                        % for direction in sorted({t.direction for t in trips}):
                            % direction_trips = [t for t in trips if t.direction == direction]
                            <div class="section">
                                <div class="header" onclick="toggleSection(this)">
                                    <h3>{{ direction }}</h3>
                                    % include('components/toggle')
                                </div>
                                <div class="content">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th class="non-mobile">Start Time</th>
                                                <th class="mobile-only">Start</th>
                                                <th class="non-mobile">Headsign</th>
                                                <th class="non-mobile">Block</th>
                                                <th>Trip</th>
                                                <th class="desktop-only">First Stop</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % last_start_time = None
                                            % for trip in direction_trips:
                                                % first_stop = trip.first_departure.stop
                                                % start_time = trip.start_time
                                                % if not start_time.is_unknown and not last_start_time:
                                                    % last_start_time = start_time
                                                % end
                                                <tr class="{{'divider' if start_time.hour > last_start_time.hour else ''}}">
                                                    <td>{{ trip.start_time.format_web(time_format) }}</td>
                                                    <td class="non-mobile">
                                                        % include('components/headsign')
                                                    </td>
                                                    <td class="non-mobile">
                                                        % block = trip.block
                                                        <a href="{{ get_url(block.system, 'blocks', block) }}">{{ block.id }}</a>
                                                    </td>
                                                    <td>
                                                        <div class="column">
                                                            % include('components/trip')
                                                            <span class="mobile-only smaller-font">
                                                                % include('components/headsign')
                                                            </span>
                                                        </div>
                                                    </td>
                                                    <td class="desktop-only">
                                                        % include('components/stop', stop=first_stop)
                                                    </td>
                                                </tr>
                                                % last_start_time = start_time
                                            % end
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        % end
                    </div>
                % else:
                    <div class="placeholder">
                        % if system.gtfs_loaded:
                            <h3>No trips found on {{ date.format_long() }}</h3>
                            <p>There are a few reasons why that might be the case:</p>
                            <ol>
                                <li>It may be a day of the week that does not normally have service</li>
                                <li>It may be a holiday in which all regular service is suspended</li>
                                <li>It may be outside of the date range for which schedules are currently available</li>
                            </ol>
                            <p>Please check again later!</p>
                        % else:
                            <h3>Trips for this route are unavailable</h3>
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>
