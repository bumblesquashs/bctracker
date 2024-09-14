
% rebase('base')

<div id="page-header">
    <h1>Blocks</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'blocks') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Schedule</span>
    </div>
</div>

% if system:
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
                            <a class="icon button" href="{{ get_url(system, f'blocks/schedule/{previous_date.format_db()}') }}">
                                % include('components/svg', name='left')
                            </a>
                            <div class="centred">
                                <h3>{{ date.format_long() }}</h3>
                                <a href="{{ get_url(system, 'blocks/schedule') }}">Go to weekly schedule</a>
                            </div>
                            <a class="icon button" href="{{ get_url(system, f'blocks/schedule/{next_date.format_db()}') }}">
                                % include('components/svg', name='right')
                            </a>
                        </div>
                        <div class="section">
                            % include('components/sheet_list', sheets=system.get_sheets(), schedule_path='blocks/schedule')
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
                    % blocks = sorted([b for b in system.get_blocks() if date in b.schedule], key=lambda b: (b.get_start_time(date=date), b.get_end_time(date=date)))
                    % if blocks:
                        <table>
                            <thead>
                                <tr>
                                    <th>Block</th>
                                    <th>Routes</th>
                                    <th class="non-mobile">Start Time</th>
                                    <th class="non-mobile">End Time</th>
                                    <th class="mobile-only">Time</th>
                                    <th class="desktop-only">Duration</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for block in blocks:
                                    % start_time = block.get_start_time(date=date).format_web(time_format)
                                    % end_time = block.get_end_time(date=date).format_web(time_format)
                                    <tr>
                                        <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                        <td>
                                            % include('components/route_list', routes=block.get_routes(date=date))
                                        </td>
                                        <td class="non-mobile">{{ start_time }}</td>
                                        <td class="non-mobile">{{ end_time }}</td>
                                        <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                                        <td class="desktop-only">{{ block.get_duration(date=date) }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    % else:
                        <div class="placeholder">
                            % if system.gtfs_loaded:
                                <h3>No blocks found for {{ system }} on {{ date.format_long() }}</h3>
                                <p>There are a few reasons why that might be the case:</p>
                                <ol>
                                    <li>It may be a day of the week that does not normally have service</li>
                                    <li>It may be a holiday in which all regular service is suspended</li>
                                    <li>It may be outside of the date range for which schedules are currently available</li>
                                </ol>
                                <p>Please check again later!</p>
                            % else:
                                <h3>Block information for {{ system }} is unavailable</h3>
                                <p>System data is currently loading and will be available soon.</p>
                            % end
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
% else:
    <div class="placeholder">
        <p>
            Blocks can only be viewed for individual systems.
            Please choose a system.
        </p>
        <div class="non-desktop">
            % include('components/systems')
        </div>
    </div>
% end
