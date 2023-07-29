
% from models.date import Date

% rebase('base')

<div class="page-header">
    <h1 class="title">Blocks</h1>
</div>

% if system is None:
    <p>Choose a system to see blocks.</p>
    <table class="striped">
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
                    <tr class="section">
                        <td colspan="3">
                            {{ region }}
                        </td>
                    </tr>
                    <tr class="display-none"></tr>
                    % for region_system in region_systems:
                        % count = len(region_system.get_blocks())
                        <tr>
                            <td>
                                <div class="flex-column">
                                    <a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
                                    <span class="mobile-only smaller-font">
                                        % if count == 1:
                                            1 Block
                                        % else:
                                            {{ count }} Blocks
                                        % end
                                    </span>
                                </div>
                            </td>
                            <td class="non-mobile">{{ count }}</td>
                            <td>
                                % include('components/weekdays_indicator', schedule=region_system.schedule, compact=True, url=get_url(region_system, 'blocks'))
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
        % sheet = sheets[0]
        <div class="flex-container">
            <div class="sidebar container flex-1">
                <div class="section">
                    <div class="header">
                        <h2>Overview</h2>
                    </div>
                    <div class="content">
                        <div class="info-box">
                            <div class="section vertical-align">
                                % if sheet == sheets[0]:
                                    <div class="button disabled">&lt;</div>
                                % else:
                                    <div class="button">&lt;</div>
                                % end
                                <div class="name centred">
                                    <h3>{{ sheet }}</h3>
                                    <a href="{{ get_url(system, f'blocks/schedule/{Date.today().format_db()}') }}">Go to today's schedule</a>
                                </div>
                                % if sheet == sheets[-1]:
                                    <div class="button disabled">&gt;</div>
                                % else:
                                    <div class="button">&gt;</div>
                                % end
                            </div>
                            <div class="section no-flex">
                                % include('components/schedule_indicator', schedule=sheet.schedule, url=get_url(system, 'blocks'), date_url=get_url(system, 'blocks/schedule'))
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex-3">
                <h2>{{ sheet }}</h2>
                <div class="container inline">
                    % service_groups = sheet.get_service_groups()
                    % for service_group in service_groups:
                        <div class="section">
                            <div class="header">
                                % for weekday in service_group.schedule.weekdays:
                                    <div id="{{ weekday.short_name }}"></div>
                                % end
                                <h3>{{ service_group }}</h3>
                            </div>
                            <div class="content">
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
                                            % start_time = block.get_start_time(service_group=service_group).format_web(time_format)
                                            % end_time = block.get_end_time(service_group=service_group).format_web(time_format)
                                            <tr>
                                                <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                                <td>
                                                    % include('components/routes_indicator', routes=block.get_routes(service_group=service_group))
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
        
        % include('components/top_button')
    % end
% end
