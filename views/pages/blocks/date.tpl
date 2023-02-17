
% from datetime import timedelta

% rebase('base', title='Blocks', enable_reload=False)

<div class="page-header">
    <h1 class="title">Blocks</h1>
    <hr />
</div>

% if system is None:
    <p>
        Blocks can only be viewed for individual systems.
        Please choose a system.
    </p>
    <div class="non-desktop">
        % include('components/systems')
    </div>
% else:
    <div class="flex-container">
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header">
                    <h2>Overview</h2>
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section vertical-align">
                            % previous_date = date - timedelta(days=1)
                            % next_date = date + timedelta(days=1)
                            <a class="button" href="{{ get_url(system, f'blocks/schedule/{previous_date.format_db()}') }}">&lt;</a>
                            <div class="name centred">
                                <h3>{{ date.format_long() }}</h3>
                                <a href="{{ get_url(system, 'blocks') }}">Return to week view</a>
                            </div>
                            <a class="button" href="{{ get_url(system, f'blocks/schedule/{next_date.format_db()}') }}">&gt;</a>
                        </div>
                        <div class="section no-flex">
                            % include('components/schedules_indicator', schedules=[s.schedule for s in system.get_sheets()], url=get_url(system, 'blocks'), date_url=get_url(system, 'blocks/schedule'))
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container flex-3">
            <div class="section">
                <div class="header">
                    <h2>{{ date.format_long() }}</h2>
                    <h3>{{ date.weekday }}</h3>
                </div>
                <div class="content">
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
                                    % start_time = block.get_start_time(date=date).format_web(time_format)
                                    % end_time = block.get_end_time(date=date).format_web(time_format)
                                    <tr>
                                        <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                        <td>
                                            % include('components/routes_indicator', routes=block.get_routes(date=date))
                                        </td>
                                        <td class="non-mobile">{{ start_time }}</td>
                                        <td class="non-mobile">{{ end_time }}</td>
                                        <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                                        <td class="desktop-only">{{ block.get_duration(date=date) }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    % end
                </div>
            </div>
        </div>
    </div>
% end
