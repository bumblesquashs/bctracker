
% from datetime import timedelta

% rebase('base')

<div class="page-header">
    <h1 class="title">
        <div class="flex-row">
            % include('components/route_indicator')
            <div class="flex-1">{{! route.display_name }}</div>
        </div>
    </h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">Schedule</span>
    </div>
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
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header">
                    <h2>Overview</h2>
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section no-flex">
                            % include('components/schedules_indicator', schedules=[s.schedule for s in sheets], schedule_path=f'routes/{route.number}/schedule')
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container flex-3">
            % for sheet in sheets:
                <div class="section">
                    <div class="header">
                        <h2>{{ sheet }}</h2>
                    </div>
                    <div class="content">
                        <div class="container inline">
                            % service_groups = sheet.service_groups
                            % for service_group in service_groups:
                                % service_group_trips = route.get_trips(service_group=service_group)
                                <div class="section">
                                    <div class="header">
                                        % for weekday in service_group.schedule.weekdays:
                                            <div id="{{ weekday.short_name }}"></div>
                                        % end
                                        <h3>{{ service_group }}</h3>
                                    </div>
                                    <div class="content">
                                        <div class="container inline">
                                            % for direction in sorted({t.direction for t in service_group_trips}):
                                                % direction_trips = [t for t in service_group_trips if t.direction == direction]
                                                <div class="section">
                                                    <div class="header">
                                                        <h4>{{ direction }}</h4>
                                                    </div>
                                                    <div class="content">
                                                        <table class="striped">
                                                            <thead>
                                                                <tr>
                                                                    <th class="non-mobile">Start Time</th>
                                                                    <th class="mobile-only">Start</th>
                                                                    <th class="non-mobile">Headsign</th>
                                                                    <th class="non-mobile">Block</th>
                                                                    <th>Trip</th>
                                                                    <th class="desktop-only">First Stop</th>
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
                                                                        <td class="non-mobile">
                                                                            % include('components/headsign_indicator')
                                                                        </td>
                                                                        <td class="non-mobile">
                                                                            <a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a>
                                                                        </td>
                                                                        <td>
                                                                            <div class="flex-column">
                                                                                <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
                                                                                <span class="mobile-only smaller-font">
                                                                                    % include('components/headsign_indicator')
                                                                                </span>
                                                                            </div>
                                                                        </td>
                                                                        <td class="desktop-only">
                                                                            <a href="{{ get_url(first_stop.system, f'stops/{first_stop.number}') }}">{{ first_stop }}</a>
                                                                        </td>
                                                                    </tr>
                                                                    % if this_hour > last_hour:
                                                                        % last_hour = this_hour
                                                                    % end
                                                                % end
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            % end
                                        </div>
                                    </div>
                                </div>
                            % end
                        </div>
                    </div>
                </div>
            % end
        </div>
    </div>

    % include('components/top_button')
% end
