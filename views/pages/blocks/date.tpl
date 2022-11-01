
% rebase('base', title='Blocks')

<div class="page-header">
    <h1 class="title">Blocks</h1>
    <hr />
</div>

% if system is None:
    <p>Blocks can only be viewed for individual systems. Please choose a system.</p>
    <div class="non-desktop">
        % include('components/systems')
    </div>
% else:
    <h2>{{ date.format_long() }}</h2>
    <p>
        <a href="{{ get_url(system, 'blocks') }}">Return to week view</a>
    </p>
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
                    % start_time = block.get_start_time(date=date)
                    % end_time = block.get_end_time(date=date)
                    <tr>
                        <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                        <td>{{ block.get_routes_string(date=date) }}</td>
                        <td class="non-mobile">{{ start_time }}</td>
                        <td class="non-mobile">{{ end_time }}</td>
                        <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                        <td class="desktop-only">{{ block.get_duration(date=date) }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end
