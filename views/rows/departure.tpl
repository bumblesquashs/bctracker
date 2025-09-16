
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
                % if position.adherence and position.adherence.value != 0 and not position.adherence.layover:
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
    % if context.enable_blocks:
        <td class="desktop-only">
            % if block:
                <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
            % else:
                <span class="lighter-text">Loading</span>
            % end
        </td>
    % end
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
            % vehicle = recorded_today[trip.id]
            <td>
                <div class="column">
                    <div class="row">
                        % include('components/vehicle')
                        % if trip.id in positions:
                            % position = positions[trip.id]
                            <div class="row gap-5">
                                % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                % include('components/adherence', adherence=position.adherence)
                            </div>
                        % end
                    </div>
                    <span class="non-desktop smaller-font">
                        % include('components/year_model', year_model=vehicle.year_model)
                    </span>
                </div>
            </td>
            <td class="desktop-only">
                % include('components/year_model', year_model=vehicle.year_model)
            </td>
        % elif trip.block_id in assignments and trip.end_time.is_later:
            % assignment = assignments[trip.block_id]
            % vehicle = assignment.vehicle
            <td>
                <div class="column">
                    <div class="row">
                        % include('components/vehicle')
                        % include('components/scheduled')
                    </div>
                    <span class="non-desktop smaller-font">
                        % include('components/year_model', year_model=vehicle.year_model)
                    </span>
                </div>
            </td>
            <td class="desktop-only">
                % include('components/year_model', year_model=vehicle.year_model)
            </td>
        % else:
            <td class="desktop-only lighter-text" colspan="2">Unavailable</td>
            <td class="non-desktop lighter-text">Unavailable</td>
        % end
    % end
</tr>
