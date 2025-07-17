% trip = departure.trip
% stop = departure.stop

<tr class="{{ 'table-button-target display-none' if get('hidden', False) else '' }}">
    <td>
        <div class="row">
            <div class="{{ 'timing-point' if departure.timepoint else '' }}">
                {{ departure.time.format_web(time_format) }}
            </div>
            % if position.adherence and position.adherence.value != 0:
                % expected_time = departure.time - timedelta(minutes=position.adherence.value)
                <div class="lighter-text">
                    ({{ expected_time.format_web(time_format) }})
                </div>
            % end
        </div>
    </td>
    % if stop:
        <td>
            <div class="column">
                % include('components/stop', timepoint=departure.timepoint)
                % if not departure.pickup_type.is_normal:
                    <span class="smaller-font italics">{{ departure.pickup_type }}</span>
                % elif departure == trip.last_departure:
                    <span class="smaller-font italics">No pick up</span>
                % end
                % if not departure.dropoff_type.is_normal:
                    <span class="smaller-font italics">{{ departure.dropoff_type }}</span>
                % elif departure == trip.first_departure:
                    <span class="smaller-font italics">No drop off</span>
                % end
            </div>
        </td>
    % else:
        <td class="lighter-text">Unknown</td>
    % end
</tr>