
% from models.date import Date

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

% if len(stop.departures) == 0:
    <p>There are currently no departures from this stop.</p>
    <p>
        There are a few reasons why that may be the case:
        <ol>
            <li>It may be an old stop that used to serve routes but is no longer used</li>
            <li>It may be a new stop that will soon serve routes that haven't started yet</li>
            <li>It may be used as an internal reference point in the GTFS that does not serve any routes</li>
        </ol>
        Please check again later!
    </p>
% else:
    % sheets = stop.get_sheets()
    % sheet = sheets[0]
    <div class="flex-container">
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header">
                    <h2>Overview</h2>
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section vertical-align">
                            % if sheet == sheets[0]:
                                <div class="button disabled">&lt;</div>
                            % else:
                                <div class="button">&lt;</div>
                            % end
                            <div class="name centred">
                                <h3>{{ sheet }}</h3>
                                <a href="{{ get_url(system, f'stops/{stop.number}/schedule/{Date.today().format_db()}') }}">Go to today's schedule</a>
                            </div>
                            % if sheet == sheets[-1]:
                                <div class="button disabled">&gt;</div>
                            % else:
                                <div class="button">&gt;</div>
                            % end
                        </div>
                        <div class="section no-flex">
                            % include('components/schedule_indicator', schedule=sheet.schedule, url=get_url(system, f'stops/{stop.number}/schedule'))
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex-3">
            <h2>{{ sheet }}</h2>
            <div class="container inline">
                % service_groups = sheet.get_service_groups()
                % for service_group in service_groups:
                    % departures = stop.get_departures(service_group)
                    <div class="section">
                        <div class="header">
                            % for weekday in service_group.schedule.weekdays:
                                <div id="{{ weekday.short_name }}"></div>
                            % end
                            <h3>{{ service_group }}</h3>
                        </div>
                        <div class="content">
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
                                            <td class="non-mobile"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                            <td>
                                                <div class="flex-column">
                                                    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
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
                        </div>
                    </div>
                % end
            </div>
        </div>
    </div>

    % include('components/top_button')
% end
