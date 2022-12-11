
% rebase('base', title=str(route), include_maps=True)

<div class="page-header">
    <h1 class="title">{{ route }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
    <hr />
</div>

% if len(route.trips) == 0:
    <p>There are currently no trips for this route.</p>
    <p>
        There are a few reasons why that may be the case:
        <ol>
            <li>It may be an old route that is no longer in service</li>
            <li>It may be a new route that hasn't started service yet</li>
            <li>It may be used as an internal route in the GTFS that does not run any trips</li>
        </ol>
        Please check again later!
    </p>
% else:
    % sheets = route.sheets
    <div class="flex-container">
        <div class="sidebar flex-1">
            <h2>Overview</h2>
            <div class="info-box">
                <div class="section no-flex">
                    % include('components/schedules_indicator', schedules=[s.schedule for s in sheets], url=get_url(system, f'routes/{route.number}/schedule'))
                </div>
            </div>
        </div>
        <div class="container flex-3">
            % for (i, sheet) in enumerate(sheets):
                % if len(sheet.service_groups) > 0:
                    % url_suffix = '' if i == 0 else f'{i + 1}'
                    <div class="section">
                        <h2>{{ sheet }}</h2>
                        <div class="container">
                            % for service_group in sheet.service_groups:
                                % service_group_trips = route.get_trips(service_group=service_group)
                                <div class="section">
                                    % for weekday in service_group.schedule.weekdays:
                                        <div id="{{ weekday.short_name }}{{ url_suffix }}"></div>
                                    % end
                                    <h3 class="title">{{ service_group }}</h3>
                                    <div class="container">
                                        % for direction in sorted({t.direction for t in service_group_trips}):
                                            % direction_trips = [t for t in service_group_trips if t.direction == direction]
                                            <div class="section">
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
                                </div>
                            % end
                        </div>
                    </div>
                % end
            % end
        </div>
    </div>

    % include('components/top_button')
% end
