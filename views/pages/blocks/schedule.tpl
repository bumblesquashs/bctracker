
% rebase('base')

<div id="page-header">
    <h1>Blocks</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'blocks') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Schedule</span>
    </div>
</div>

% if context.system:
    % blocks = context.system.get_blocks()
    % if blocks:
        % sheets = context.system.get_sheets()
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
                                % include('components/sheet_list', schedule_path='blocks/schedule')
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container inline flex-3">
                % for (i, sheet) in enumerate(sheets):
                    % sheet_blocks = [b for b in blocks if [t for t in b.trips if t.service in sheet.services]]
                    % if not sheet_blocks:
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
                                                    % service_group_blocks = sorted([b for b in blocks if b.get_trips(service_group)], key=lambda b: (b.get_start_time(service_group=service_group), b.get_end_time(service_group=service_group)))
                                                    % for block in service_group_blocks:
                                                        % start_time = block.get_start_time(service_group=service_group).format_web(time_format)
                                                        % end_time = block.get_end_time(service_group=service_group).format_web(time_format)
                                                        <tr>
                                                            <td><a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a></td>
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
    % else:
        <div class="placeholder">
            <h3>{{ context }} block information is unavailable</h3>
            % if context.gtfs_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        </div>
    % end
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
                        % for system in sorted(region_systems):
                            % count = len(system.get_blocks())
                            <tr>
                                <td>
                                    <div class="row">
                                        % include('components/agency_logo', agency=system.agency)
                                        <div class="column">
                                            <a href="{{ get_url(system.context, *path) }}">{{ system }}</a>
                                            <span class="mobile-only smaller-font">
                                                % if system.gtfs_loaded:
                                                    % if count == 1:
                                                        1 Block
                                                    % else:
                                                        {{ count }} Blocks
                                                    % end
                                                % end
                                            </span>
                                        </div>
                                    </div>
                                </td>
                                % if system.gtfs_loaded:
                                    <td class="non-mobile align-right">{{ count }}</td>
                                    <td>
                                        % include('components/weekdays', schedule=system.schedule, compact=True, schedule_path='blocks')
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
