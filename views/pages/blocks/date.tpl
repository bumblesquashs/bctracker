
% from datetime import timedelta

% rebase('base', title='Blocks')

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
    % blocks = [b for b in system.get_blocks() if b.schedule.includes(date)]
    <div class="flex-container">
        <div class="sidebar flex-1">
            <h2>Overview</h2>
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
            % if len(blocks) > 0:
                <h2>Trip Distribution</h2>
                <style>
                    .block-display {
                        position: flex;
                        flex-direction: column;
                    }
                    
                    .block-display .block {
                        position: relative;
                        height: 5px;
                    }
                    
                    .block-display .block .trip {
                        position: absolute;
                        height: 100%;
                    }
                </style>
                <div class="block-display">
                    % start_time = min([b.get_start_time(date=date) for b in blocks])
                    % end_time = max([b.get_end_time(date=date) for b in blocks])
                    % total_minutes = end_time.get_minutes() - start_time.get_minutes()
                    % for block in sorted(blocks, key=lambda b: b.get_start_time(date=date)):
                        <div class="block">
                            % for trip in block.get_trips(date=date):
                                % trip_minutes = trip.end_time.get_minutes() - trip.start_time.get_minutes()
                                % percentage = (trip_minutes / total_minutes) * 100
                                % offset_minutes = trip.start_time.get_minutes() - start_time.get_minutes()
                                % offset_percentage = (offset_minutes / total_minutes) * 100
                                <div class="trip" style="background-color: #{{ trip.route.colour }}; width: {{ percentage }}%; left: {{ offset_percentage }}%;">
                                    
                                </div>
                            % end
                        </div>
                    % end
                </div>
            % end
        </div>
        <div class="flex-3">
            <h2>{{ date.format_long() }}</h2>
            <h3>{{ date.weekday }}</h3>
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
                                    % include('components/route_indicator', routes=block.get_routes(date=date))
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
% end
