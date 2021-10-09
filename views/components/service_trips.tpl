<table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
        <tr>
            <th class="non-mobile">Start Time</th>
            <th class="mobile-only">Start</th>
            <th>Headsign</th>
            <th class="desktop-only">Departing From</th>
            <th class="desktop-only">Block</th>
            <th>Trip</th>
        </tr>
    </thead>
    <tbody>
        % last_hour = -1
        % for trip in trips:
            % first_stop = trip.stop_times[0].stop
            % this_hour = trip.start_time.hour
            % if last_hour == -1:
                % last_hour = this_hour
            % end
            <tr class="{{'divider' if this_hour > last_hour else ''}}">
                <td>{{ trip.start_time }}</td>
                <td>{{ trip }}</td>
                <td class="desktop-only"><a href="{{ get_url(first_stop.system, f'stops/{first_stop.number}') }}">{{ first_stop }}</a></td>
                <td class="desktop-only"><a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a></td>
                <td><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
            </tr>
            % if this_hour > last_hour:
                % last_hour = this_hour
            % end
        % end
    </tbody>
</table>
