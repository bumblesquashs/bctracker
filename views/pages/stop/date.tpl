
% rebase('base')

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }}</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'stops/{stop.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'stops/{stop.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
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
                        % previous_date = date.previous()
                        % next_date = date.next()
                        <a class="button" href="{{ get_url(system, f'stops/{stop.number}/schedule/{previous_date.format_db()}') }}">&lt;</a>
                        <div class="name centred">
                            <h3>{{ date.format_long() }}</h3>
                            <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}">Return to week view</a>
                        </div>
                        <a class="button" href="{{ get_url(system, f'stops/{stop.number}/schedule/{next_date.format_db()}') }}">&gt;</a>
                    </div>
                    <div class="section no-flex">
                        % include('components/sheets_indicator', sheets=stop.sheets, schedule_path=f'stops/{stop.number}/schedule')
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
                    <div class="placeholder">
                        % if system.is_loaded:
                            <h3 class="title">No departures found on {{ date.format_long() }}</h3>
                            <p>There are a few reasons why that might be the case:</p>
                            <ol>
                                <li>It may be a day of the week that does not normally have service</li>
                                <li>It may be a holiday in which all regular service is suspended</li>
                                <li>It may be outside of the date range for which schedules are currently available</li>
                            </ol>
                            <p>Please check again later!</p>
                        % else:
                            <h3 class="title">Departures for this stop are unavailable</h3>
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
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
                                        <div class="flex-column">
                                            % include('components/headsign_indicator')
                                            % if not departure.pickup_type.is_normal:
                                                <span class="smaller-font">{{ departure.pickup_type }}</span>
                                            % elif departure == trip.last_departure:
                                                <span class="smaller-font">Drop off only</span>
                                            % end
                                            % if not departure.dropoff_type.is_normal:
                                                <span class="smaller-font">{{ departure.dropoff_type }}</span>
                                            % end
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % if block is None:
                                            <div class="lighter-text">Unknown</div>
                                        % else:
                                            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                        % end
                                    </td>
                                    <td>
                                        <div class="flex-column">
                                            % include('components/trip_link', trip=trip)
                                            <span class="mobile-only smaller-font">
                                                % include('components/headsign_indicator')
                                            </span>
                                            % if not departure.pickup_type.is_normal:
                                                <span class="mobile-only smaller-font">{{ departure.pickup_type }}</span>
                                            % elif departure == trip.last_departure:
                                                <span class="mobile-only smaller-font">Drop off only</span>
                                            % end
                                            % if not departure.dropoff_type.is_normal:
                                                <span class="mobile-only smaller-font">{{ departure.dropoff_type }}</span>
                                            % end
                                        </div>
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
