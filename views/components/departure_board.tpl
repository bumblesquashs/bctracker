% import helpers

% hours = sorted({d.time.hour for d in departures})
% if hours:
    % min_hour = min(hours)
    % max_hour = max(hours)
    <table>
        <thead>
            <tr>
                <th colspan="2">Departures</th>
            </tr>
        </thead>
        <tbody>
            % for hour in range(min_hour, max_hour + 1):
                % hour_departures = sorted([d for d in departures if d.time.hour == hour])
                <tr>
                    <td>
                        <div class="departure-hour">{{ helpers.format_hour(hour, time_format) }}{{ '' if time_format == '12hr' else ':' }}</div>
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
% end
