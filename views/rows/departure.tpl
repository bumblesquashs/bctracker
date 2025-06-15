
% from datetime import timedelta

% trip = departure.trip

% show_divider = get('show_divider', False)
% show_time_estimate = get('show_time_estimate', False)

<tr class="{{'divider' if show_divider else ''}}">
    <td>
        % if show_time_estimate:
            % expected_time = None
            % if trip.id in positions:
                % position = positions[trip.id]
                % if position.adherence and position.adherence.value != 0:
                    % expected_time = departure.time - timedelta(minutes=position.adherence.value)
                % end
            % end
            % if expected_time:
                <div class="row non-mobile">
                    {{ departure.time.format_web(time_format) }}
                    <div class="lighter-text">({{ expected_time.format_web(time_format) }})</div>
                </div>
                <div class="column mobile-only">
                    {{ departure.time.format_web(time_format) }}
                    <div class="lighter-text smaller-font">({{ expected_time.format_web(time_format) }})</div>
                </div>
            % else:
                {{ departure.time.format_web(time_format) }}
            % end
        % else:
            {{ departure.time.format_web(time_format) }}
        % end
    </td>
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
    <td class="desktop-only">
        <a href="{{ get_url(trip.context, 'blocks', trip.block_id) }}">{{ trip.block_id }}</a>
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
    % if context.realtime_enabled:
        % if trip.id in recorded_today:
            % bus = recorded_today[trip.id]
            <td>
                <div class="column">
                    <div class="row">
                        % include('components/bus')
                        % if trip.id in positions:
                            % position = positions[trip.id]
                            <div class="row gap-5">
                                % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                % include('components/adherence', adherence=position.adherence)
                            </div>
                        % end
                    </div>
                    <span class="non-desktop smaller-font">
                        % include('components/order', order=bus.order)
                    </span>
                </div>
            </td>
            <td class="desktop-only">
                % include('components/order', order=bus.order)
            </td>
        % elif (trip.context.system_id, trip.block_id) in assignments and trip.end_time.is_later:
            % assignment = assignments[(trip.context.system_id, trip.block_id)]
            % bus = assignment.bus
            <td>
                <div class="column">
                    <div class="row">
                        % include('components/bus')
                        % include('components/scheduled')
                    </div>
                    <span class="non-desktop smaller-font">
                        % include('components/order', order=bus.order)
                    </span>
                </div>
            </td>
            <td class="desktop-only">
                % include('components/order', order=bus.order)
            </td>
        % else:
            <td class="desktop-only lighter-text" colspan="2">Unavailable</td>
            <td class="non-desktop lighter-text">Unavailable</td>
        % end
    % end
</tr>