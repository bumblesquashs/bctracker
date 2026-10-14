% import helpers

% hours = sorted({d.time.hour for d in departures})
<table>
    <thead>
        <tr>
            <th colspan="2">Departures</th>
        </tr>
    </thead>
    <tbody>
        % for hour in hours:
            % hour_departures = sorted([d for d in departures if d.time.hour == hour])
            <tr>
                <td>
                    <div class="departure-hour">{{ helpers.format_hour(hour, time_format) }}</div>
                </td>
                <td>
                    <div class="departure-list">
                        % for departure in hour_departures:
                            % include('components/departure')
                        % end
                    </div>
                </td>
            </tr>
        % end
    </tbody>
</table>
