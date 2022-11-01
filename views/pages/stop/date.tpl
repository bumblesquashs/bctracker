
% rebase('base', title='Blocks')

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

<h2>{{ date.format_long() }}</h2>
<p>
    <a href="{{ get_url(system, f'stops/{stop.number}/schedule') }}">Return to week view</a>
</p>

% departures = [d for d in stop.departures if d.trip.service.schedule.includes(date)]
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
                    <td>{{ departure.time }}</td>
                    <td class="non-mobile">
                        {{ trip }}
                        % if departure == trip.last_departure:
                            <br />
                            <span class="smaller-font">Unloading only</span>
                        % end
                    </td>
                    <td class="non-mobile"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                    <td>
                        <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                        <br class="mobile-only" />
                        <span class="mobile-only smaller-font">{{ trip }}</span>
                        % if departure == trip.last_departure:
                            <br class="mobile-only" />
                            <span class="mobile-only smaller-font">Unloading only</span>
                        % end
                    </td>
                </tr>
                % last_hour = this_hour
            % end
        </tbody>
    </table>
% end