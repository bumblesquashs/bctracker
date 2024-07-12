
% rebase('base')

<div id="page-header">
    <h1>Blocks</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, 'blocks/schedule') }}" class="tab-button">Schedule</a>
    </div>
</div>

% if system:
    % blocks = system.get_blocks()
    % today_blocks = sorted([b for b in blocks if today in b.schedule], key=lambda b: (b.get_start_time(date=today), b.get_end_time(date=today)))
    % blocks_so_far = [b for b in today_blocks if b.get_start_time(date=today) <= now]
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
                            % include('components/sheet_list', sheets=system.get_sheets(), schedule_path='blocks/schedule')
                        </div>
                        % if today_blocks:
                            <h3 class="title">Today</h3>
                            <div class="section row">
                                <div class="name">Service Starts</div>
                                <div class="value">
                                    % start_times = [b.get_start_time(date=today) for b in today_blocks]
                                    {{ min(start_times).format_web(time_format) }}
                                </div>
                            </div>
                            <div class="section row">
                                <div class="name">Service Ends</div>
                                <div class="value">
                                    % end_times = [b.get_end_time(date=today) for b in today_blocks]
                                    {{ max(end_times).format_web(time_format) }}
                                </div>
                            </div>
                            <div class="section row">
                                <div class="name">Total Blocks</div>
                                <div class="value">{{ len(today_blocks) }}</div>
                            </div>
                            % if system.realtime_enabled:
                                <div class="section row">
                                    <div class="name column">
                                        <div>Assigned Buses</div>
                                        <div class="lighter-text smaller-font">As of {{ now.format_web(time_format) }}</div>
                                    </div>
                                    <div class="value">
                                        % include('components/percentage', numerator=len([b for b in blocks_so_far if b.id in recorded_buses]), denominator=len(blocks_so_far), low_cutoff=70, high_cutoff=90)
                                    </div>
                                </div>
                            % end
                        % end
                    </div>
                </div>
            </div>
        </div>
        <div class="container inline flex-3">
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Today's Schedule</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Block</th>
                                <th>Routes</th>
                                <th class="non-mobile">Start Time</th>
                                <th class="non-mobile">End Time</th>
                                <th class="mobile-only">Time</th>
                                <th class="desktop-only">Duration</th>
                                % if system.realtime_enabled:
                                    <th class="desktop-only">Bus</th>
                                    <th class="desktop-only">Model</th>
                                % end
                            </tr>
                        </thead>
                        <tbody>
                            % for block in today_blocks:
                                % start_time = block.get_start_time(date=today).format_web(time_format)
                                % end_time = block.get_end_time(date=today).format_web(time_format)
                                <tr>
                                    <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                    <td>
                                        % include('components/route_list', routes=block.get_routes(date=today))
                                    </td>
                                    <td class="non-mobile">{{ start_time }}</td>
                                    <td class="non-mobile">{{ end_time }}</td>
                                    <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                                    <td class="desktop-only">{{ block.get_duration(date=today) }}</td>
                                    % if system.realtime_enabled:
                                        % if block.id in recorded_buses:
                                            % bus = recorded_buses[block.id]
                                            <td>
                                                <div class="column">
                                                    % include('components/bus')
                                                    <span class="non-desktop smaller-font">
                                                        % include('components/order', order=bus.order)
                                                    </span>
                                                </div>
                                            </td>
                                            <td class="desktop-only">
                                                % include('components/order', order=bus.order)
                                            </td>
                                        % else:
                                            <td class="desktop-only lighter-text" colspan="2">Unavailable</td>
                                        % end
                                    % end
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    % include('components/top_button')
% else:
    <div class="placeholder">
        <p>Choose a system to see blocks.</p>
        <table>
            <thead>
                <tr>
                    <th>System</th>
                    <th class="non-mobile align-right">Blocks</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if region_systems:
                        <tr class="header">
                            <td colspan="3">{{ region }}</td>
                        </tr>
                        <tr class="display-none"></tr>
                        % for region_system in sorted(region_systems):
                            % count = len(region_system.get_blocks())
                            <tr>
                                <td>
                                    <div class="column">
                                        <a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
                                        <span class="mobile-only smaller-font">
                                            % if region_system.gtfs_loaded:
                                                % if count == 1:
                                                    1 Block
                                                % else:
                                                    {{ count }} Blocks
                                                % end
                                            % end
                                        </span>
                                    </div>
                                </td>
                                % if region_system.gtfs_loaded:
                                    <td class="non-mobile align-right">{{ count }}</td>
                                    <td>
                                        % include('components/weekdays', schedule=region_system.schedule, compact=True, schedule_path='blocks')
                                    </td>
                                % else:
                                    <td class="lighter-text" colspan="2">Blocks are loading...</td>
                                % end
                            </tr>
                        % end
                    % end
                % end
            </tbody>
        </table>
    </div>
% end
