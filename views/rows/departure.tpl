
% trip = departure.trip
% block = trip.block

% show_divider = get('show_divider', False)

<tr class="{{'divider' if show_divider else ''}}">
    <td>{{ departure.time.format_web(time_format) }}</td>
    % if system is None or system.realtime_enabled:
        % if trip.id in recorded_today:
            % bus = recorded_today[trip.id]
            % order = bus.order
            <td>
                <div class="flex-column">
                    <div class="flex-row left">
                        % include('components/bus', bus=bus)
                        % if trip.id in positions:
                            % position = positions[trip.id]
                            % include('components/adherence_indicator', adherence=position.adherence)
                        % end
                    </div>
                    <span class="non-desktop smaller-font">
                        % include('components/order', order=order)
                    </span>
                </div>
            </td>
            <td class="desktop-only">
                % include('components/order', order=order)
            </td>
        % elif trip.block_id in scheduled_today and trip.start_time.is_later:
            % bus = scheduled_today[trip.block_id]
            % order = bus.order
            <td>
                <div class="flex-column">
                    <div class="flex-row left">
                        % include('components/bus', bus=bus)
                        <div class="tooltip-anchor">
                            <img class="middle-align white" src="/img/white/schedule.png" />
                            <img class="middle-align black" src="/img/black/schedule.png" />
                            <div class="tooltip">Bus is scheduled</div>
                        </div>
                    </div>
                    <span class="non-desktop smaller-font">
                        % include('components/order', order=order)
                    </span>
                </div>
            </td>
            <td class="desktop-only">
                % include('components/order', order=order)
            </td>
        % else:
            <td class="desktop-only lighter-text" colspan="2">Unavailable</td>
            <td class="non-desktop lighter-text">Unavailable</td>
        % end
    % end
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
    <td class="desktop-only">
        <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
    </td>
    <td>
        <div class="flex-column">
            <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
            <span class="mobile-only smaller-font">
                % include('components/headsign_indicator')
            </span>
        </div>
    </td>
</tr>