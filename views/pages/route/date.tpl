
% from datetime import timedelta

% rebase('base', title='Blocks')

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
    <hr />
</div>

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div>
            <h2>Overview</h2>
            <div class="info-box">
                <div class="section vertical-align">
                    % previous_date = date - timedelta(days=1)
                    % next_date = date + timedelta(days=1)
                    <a class="button" href="{{ get_url(system, f'routes/{route.number}/schedule/{previous_date.format_db()}') }}">&lt;</a>
                    <div class="name centred">
                        <h3>{{ date.format_long() }}</h3>
                        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}">Return to week view</a>
                    </div>
                    <a class="button" href="{{ get_url(system, f'routes/{route.number}/schedule/{next_date.format_db()}') }}">&gt;</a>
                </div>
                <div class="section no-flex">
                    % include('components/schedules_indicator', schedules=[s.schedule for s in route.sheets], url=get_url(system, f'routes/{route.number}/schedule'))
                </div>
            </div>
        </div>
    </div>
    <div class="container flex-3">
        <div>
            <h2>{{ date.format_long() }}</h2>
            <h3>{{ date.weekday }}</h3>
            % trips = route.get_trips(date=date)
            % if len(trips) == 0:
                <p>No trips found on {{ date.format_long() }}.</p>
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
                <div class="container inline">
                    % for direction in sorted({t.direction for t in trips}):
                        % direction_trips = [t for t in trips if t.direction == direction]
                        <div>
                            <h4>{{ direction }}</h4>
                            <table class="striped">
                                <thead>
                                    <tr>
                                        <th class="non-mobile">Start Time</th>
                                        <th class="mobile-only">Start</th>
                                        <th class="non-mobile">Headsign</th>
                                        <th class="desktop-only">Departing From</th>
                                        <th class="non-mobile">Block</th>
                                        <th>Trip</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % last_hour = -1
                                    % for trip in direction_trips:
                                        % first_stop = trip.first_departure.stop
                                        % this_hour = trip.start_time.hour
                                        % if last_hour == -1:
                                            % last_hour = this_hour
                                        % end
                                        <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                            <td>{{ trip.start_time.format_web(time_format) }}</td>
                                            <td class="non-mobile">{{ trip }}</td>
                                            <td class="desktop-only"><a href="{{ get_url(first_stop.system, f'stops/{first_stop.number}') }}">{{ first_stop }}</a></td>
                                            <td class="non-mobile"><a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a></td>
                                            <td>
                                                <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                                <br class="mobile-only" />
                                                <span class="mobile-only smaller-font">{{ trip }}</span>
                                            </td>
                                        </tr>
                                        % if this_hour > last_hour:
                                            % last_hour = this_hour
                                        % end
                                    % end
                                </tbody>
                            </table>
                        </div>
                    % end
                </div>
            % end
        </div>
    </div>
</div>
