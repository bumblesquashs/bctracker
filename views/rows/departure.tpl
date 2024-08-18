
% from datetime import timedelta

% trip = departure.trip
% block = trip.block

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
    % if not system or system.realtime_enabled:
        % if trip.id in recorded_today:
            % bus = recorded_today[trip.id]
            <td>
                <div class="column">
                    <div class="row gap-5">
                        % include('components/bus')
                        % if trip.id in positions:
                            % position = positions[trip.id]
                            % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                            % include('components/adherence', adherence=position.adherence)
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
        % elif (trip.system.id, trip.block_id) in assignments and trip.end_time.is_later:
            % assignment = assignments[(trip.system.id, trip.block_id)]
            % bus = assignment.bus
            <td>
                <div class="column">
                    <div class="row gap-5">
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
    <td class="non-mobile">
        <div class="column">
            % include('components/headsign')
            % if not departure.pickup_type.is_normal:
                <span class="smaller-font">{{ departure.pickup_type }}</span>
            % elif departure == trip.last_departure:
                <span class="smaller-font">No pick up</span>
            % end
            % if not departure.dropoff_type.is_normal:
                <span class="smaller-font">{{ departure.dropoff_type }}</span>
            % end
        </div>
    </td>
    <td class="desktop-only">
        % if block:
            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
        % else:
            <span class="lighter-text">Loading</span>
        % end
    </td>
    <td>
        <div class="column">
            % include('components/trip')
            <span class="mobile-only smaller-font">
                % include('components/headsign')
            </span>
        </div>
    </td>
</tr>