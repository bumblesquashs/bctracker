
% trip = departure.trip
% block = trip.block

% show_divider = get('show_divider', False)

<tr class="{{'divider' if show_divider else ''}}">
    <td>{{ departure.time.format_web(time_format) }}</td>
    % if system is None or system.realtime_enabled:
        % if trip.id in recorded_today:
            % bus = recorded_today[trip.id]
            <td>
                <div class="column">
                    <div class="row">
                        % include('components/bus')
                        % if trip.id in positions:
                            % position = positions[trip.id]
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
        % elif trip.block_id in scheduled_today and trip.start_time.is_later:
            % bus = scheduled_today[trip.block_id]
            <td>
                <div class="column">
                    <div class="row">
                        % include('components/bus')
                        <div class="tooltip-anchor">
                            <img class="middle-align white" src="/img/white/schedule.png" />
                            <img class="middle-align black" src="/img/black/schedule.png" />
                            <div class="tooltip right">Bus is scheduled</div>
                        </div>
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
        % if block is None:
            <span class="lighter-text">Loading</span>
        % else:
            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
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