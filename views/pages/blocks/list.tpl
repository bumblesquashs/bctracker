
% rebase('base')

<div id="page-header">
    <h1>Blocks</h1>
</div>

% if system is None:
    <div class="placeholder">
        <p>Choose a system to see blocks.</p>
        <table>
            <thead>
                <tr>
                    <th>System</th>
                    <th class="non-mobile"># Blocks</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if len(region_systems) > 0:
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
                                    <td class="non-mobile">{{ count }}</td>
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
% else:
    % blocks = system.get_blocks()
    % if len(blocks) == 0:
        <div class="placeholder">
            <h3>Block information for {{ system }} is unavailable</h3>
            % if system.gtfs_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        </div>
    % else:
        % sheets = system.get_sheets()
        <div class="page-container">
            <div class="sidebar container flex-1">
                <div class="section">
                    <div class="header">
                        <h2>Overview</h2>
                    </div>
                    <div class="content">
                        <div class="info-box">
                            <div class="section">
                                % include('components/sheet_list', schedule_path='blocks', date_path='blocks/schedule')
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container inline flex-3">
                % for (i, sheet) in enumerate(sheets):
                    % path_suffix = '' if i == 0 else str(i + 1)
                    <div class="section">
                        <div class="header">
                            <h2>{{ sheet }}</h2>
                        </div>
                        <div class="content">
                            <div class="container inline">
                                % for service_group in sheet.normal_service_groups:
                                    <div class="section">
                                        <div class="header">
                                            % for weekday in service_group.schedule.weekdays:
                                                <div id="{{ weekday.short_name }}{{path_suffix}}"></div>
                                            % end
                                            <h3>{{ service_group }}</h3>
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
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    % service_group_blocks = sorted([b for b in blocks if len(b.get_trips(service_group)) > 0], key=lambda b: (b.get_start_time(service_group=service_group), b.get_end_time(service_group=service_group)))
                                                    % for block in service_group_blocks:
                                                        % start_time = block.get_start_time(service_group=service_group).format_web(time_format)
                                                        % end_time = block.get_end_time(service_group=service_group).format_web(time_format)
                                                        <tr>
                                                            <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                                            <td>
                                                                % include('components/route_list', routes=block.get_routes(service_group=service_group))
                                                            </td>
                                                            <td class="non-mobile">{{ start_time }}</td>
                                                            <td class="non-mobile">{{ end_time }}</td>
                                                            <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                                                            <td class="desktop-only">{{ block.get_duration(service_group=service_group) }}</td>
                                                        </tr>
                                                    % end
                                                </tbody>
                                            </table>
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
    % end
% end
