
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
                                % include('components/schedule_indicator', schedule=region_system.schedule, compact=True, url=get_url(region_system, 'blocks'))
                            </td>
                        </tr>
                    % end
                % end
            % end
        </tbody>
    </table>
% else:
    <h2>{{ date.format_long() }}</h2>
    <a href="{{ get_url(system, 'blocks') }}">Return to week view</a>
    % blocks = [b for b in system.get_blocks() if b.schedule.includes(date)]
    % if len(blocks) == 0:
        <p>No blocks found for {{ system }} on {{ date.format_long() }}.</p>
        <p>
            There are a few reasons why that might be the case:
            <ol>
                <li>It may be a day of the week that does not normally have service</li>
                <li>It may be a holiday in which all regular service is suspended</li>
                <li>It may be outside of the date range for which schedules are currently available</li>
            </ol>
            Please check again later!
        </p>
    % else:
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
                % for block in blocks:
                    % start_time = block.get_start_time()
                    % end_time = block.get_end_time()
                    <tr>
                        <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                        <td>{{ block.get_routes_string() }}</td>
                        <td class="non-mobile">{{ start_time }}</td>
                        <td class="non-mobile">{{ end_time }}</td>
                        <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                        <td class="desktop-only">{{ block.get_duration() }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end
