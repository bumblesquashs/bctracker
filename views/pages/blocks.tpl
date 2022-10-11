
% rebase('base', title='Blocks')

<div class="page-header">
    <h1 class="title">Blocks</h1>
    <hr />
</div>

% if system is None:
    <p>Choose a system to see individual blocks.</p>
    <table class="striped">
        <thead>
            <tr>
                <th>System</th>
                <th># Blocks</th>
                <th>Service Days</th>
            </tr>
        </thead>
        <tbody>
            % for region in regions:
                % region_systems = [s for s in systems if s.region == region]
                % if len(region_systems) > 0:
                    <tr class="section">
                        <td colspan="3">
                            {{ region }}
                        </td>
                    </tr>
                    <tr class="display-none"></tr>
                    % for region_system in region_systems:
                        <tr>
                            <td><a href="{{ get_url(region_system, path) }}">{{ region_system }}</a></td>
                            <td>{{ len(region_system.get_blocks()) }}</td>
                            <td>
                                % include('components/schedule_indicator', schedule=region_system.schedule, compact=True)
                            </td>
                        </tr>
                    % end
                % end
            % end
        </tbody>
    </table>
% else:
    % blocks = system.get_blocks()
    % if len(blocks) == 0:
        <p>
            Block information is currently unavailable for {{ system }}.
            Please check again later!
        </p>
    % else:
        % sheets = system.get_sheets()
        <div class="flex-container">
            <div class="sidebar flex-1">
                <h2>Overview</h2>
                % include('components/sheet_navigation', sheets=sheets)
            </div>
            <div class="flex-3">
                <div class="container">
                    % for sheet in sheets:
                        <div class="section">
                            <h2>{{ sheet }}</h2>
                            <div class="container">
                                % for service_group in sheet.service_groups:
                                    <div class="section" id="{{ service_group.id }}">
                                        <h3 class="title">{{ service_group }}</h3>
                                        % if len(service_group.modified_dates) > 0:
                                            {{ service_group.modified_dates_string }}
                                        % end
                                        <table class="striped">
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
                                                % service_group_blocks = [b for b in blocks if len(b.get_trips(service_group)) > 0]
                                                % for block in service_group_blocks:
                                                    % start_time = block.get_start_time(service_group)
                                                    % end_time = block.get_end_time(service_group)
                                                    <tr>
                                                        <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                                        <td>{{ block.get_routes_string(service_group) }}</td>
                                                        <td class="non-mobile">{{ start_time }}</td>
                                                        <td class="non-mobile">{{ end_time }}</td>
                                                        <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                                                        <td class="desktop-only">{{ block.get_duration(service_group) }}</td>
                                                    </tr>
                                                % end
                                            </tbody>
                                        </table>
                                    </div>
                                % end
                            </div>
                        </div>
                    % end
                </div>
            </div>
        </div>
        
        % include('components/top_button')
    % end
% end
