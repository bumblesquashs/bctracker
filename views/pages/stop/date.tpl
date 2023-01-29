
% from datetime import timedelta

% rebase('base', title=f'Stop {stop.number}', enable_refresh=False)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'stops/{stop.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'stops/{stop.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
    <hr />
</div>

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
                        <a class="button" href="{{ get_url(system, f'stops/{stop.number}/schedule/{previous_date.format_db()}') }}">&lt;</a>
                        <div class="name centred">
                            <h3>{{ date.format_long() }}</h3>
                            <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}">Return to week view</a>
                        </div>
                        <a class="button" href="{{ get_url(system, f'stops/{stop.number}/schedule/{next_date.format_db()}') }}">&gt;</a>
                    </div>
                    <div class="section no-flex">
                        % include('components/schedules_indicator', schedules=[s.schedule for s in stop.sheets], url=get_url(system, f'stops/{stop.number}/schedule'))
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
                % departures = stop.get_departures(date=date)
                % if len(departures) == 0:
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
                    <table class="striped">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th class="non-mobile">Headsign</th>
                                <th class="non-mobile">Block</th>
                                <th>Trip</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_hour = -1
                            % for departure in departures:
                                % trip = departure.trip
                                % block = trip.block
                                % this_hour = departure.time.hour
                                % if last_hour == -1:
                                    % last_hour = this_hour
                                % end
                                <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                    <td>{{ departure.time.format_web(time_format) }}</td>
                                    <td class="non-mobile">
                                        {{ trip }}
                                        % if not departure.pickup_type.is_normal:
                                            <br />
                                            <span class="smaller-font">{{ departure.pickup_type }}</span>
                                        % elif departure == trip.last_departure:
                                            <br />
                                            <span class="smaller-font">Drop off only</span>
                                        % end
                                        % if not departure.dropoff_type.is_normal:
                                            <br />
                                            <span class="smaller-font">{{ departure.dropoff_type }}</span>
                                        % end
                                    </td>
                                    <td class="non-mobile"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                    <td>
                                        <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                        <br class="mobile-only" />
                                        <span class="mobile-only smaller-font">{{ trip }}</span>
                                        % if not departure.pickup_type.is_normal:
                                            <br class="mobile-only" />
                                            <span class="mobile-only smaller-font">{{ departure.pickup_type }}</span>
                                        % elif departure == trip.last_departure:
                                            <br class="mobile-only" />
                                            <span class="mobile-only smaller-font">Drop off only</span>
                                        % end
                                        % if not departure.dropoff_type.is_normal:
                                            <br class="mobile-only" />
                                            <span class="mobile-only smaller-font">{{ departure.dropoff_type }}</span>
                                        % end
                                    </td>
                                </tr>
                                % last_hour = this_hour
                            % end
                        </tbody>
                    </table>
                % end
            </div>
        </div>
    </div>
</div>
