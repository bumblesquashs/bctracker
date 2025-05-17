
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/stop', include_link=False)
        % include('components/favourite')
    </h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'stops', stop) }}" class="tab-button">Overview</a>
        <a href="{{ get_url(context, 'stops', stop, 'map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Overview</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="row section align-center">
                        % previous_date = date.previous()
                        % next_date = date.next()
                        <a class="icon button" href="{{ get_url(stop.context, 'stops', stop, 'schedule', previous_date) }}">
                            % include('components/svg', name='paging/left')
                        </a>
                        <div class="centred">
                            <h3>{{ date.format_long() }}</h3>
                            <a href="{{ get_url(stop.context, 'stops', stop, 'schedule') }}">Return to week view</a>
                        </div>
                        <a class="icon button" href="{{ get_url(stop.context, 'stops', stop, 'schedule', next_date) }}">
                            % include('components/svg', name='paging/right')
                        </a>
                    </div>
                    <div class="section">
                        % include('components/sheet_list', sheets=stop.sheets, schedule_path=f'stops/{stop.url_id}/schedule')
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <div class="column">
                    <h2>{{ date.format_long() }}</h2>
                    <p>{{ date.weekday }}</p>
                </div>
                % include('components/toggle')
            </div>
            <div class="content">
                % departures = stop.find_departures(date=date)
                % if departures:
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th class="non-mobile">Headsign</th>
                                <th class="non-mobile">Block</th>
                                <th>Trip</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_time = None
                            % for departure in departures:
                                % trip = departure.trip
                                % block = trip.block
                                % if not last_time:
                                    % last_time = departure.time
                                % end
                                <tr class="{{'divider' if departure.time.hour > last_time.hour else ''}}">
                                    <td>{{ departure.time.format_web(time_format) }}</td>
                                    <td class="non-mobile">
                                        <div class="column">
                                            % include('components/headsign')
                                            % if not departure.pickup_type.is_normal:
                                                <span class="smaller-font italics">{{ departure.pickup_type }}</span>
                                            % elif departure == trip.last_departure:
                                                <span class="smaller-font italics">No pick up</span>
                                            % end
                                            % if not departure.dropoff_type.is_normal:
                                                <span class="smaller-font italics">{{ departure.dropoff_type }}</span>
                                            % end
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % if block:
                                            <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                        % else:
                                            <div class="lighter-text">Unknown</div>
                                        % end
                                    </td>
                                    <td>
                                        <div class="column">
                                            % include('components/trip')
                                            <span class="mobile-only smaller-font">
                                                % include('components/headsign')
                                            </span>
                                            % if not departure.pickup_type.is_normal:
                                                <span class="mobile-only smaller-font italics">{{ departure.pickup_type }}</span>
                                            % elif departure == trip.last_departure:
                                                <span class="mobile-only smaller-font italics">No pick up</span>
                                            % end
                                            % if not departure.dropoff_type.is_normal:
                                                <span class="mobile-only smaller-font italics">{{ departure.dropoff_type }}</span>
                                            % end
                                        </div>
                                    </td>
                                </tr>
                                % last_time = departure.time
                            % end
                        </tbody>
                    </table>
                % else:
                    <div class="placeholder">
                        % if context.gtfs_loaded:
                            <h3>No departures found on {{ date.format_long() }}</h3>
                            <p>There are a few reasons why that might be the case:</p>
                            <ol>
                                <li>It may be a day of the week that does not normally have service</li>
                                <li>It may be a holiday in which all regular service is suspended</li>
                                <li>It may be outside of the date range for which schedules are currently available</li>
                            </ol>
                            <p>Please check again later!</p>
                        % else:
                            <h3>Departures for this stop are unavailable</h3>
                            <p>System data is currently loading and will be available soon.</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>
