
% bus = position.bus
% trip = position.trip

<tr>
    <td>
        <div class="flex-column">
            <div class="flex-row left">
                % include('components/bus', bus=bus)
                % include('components/adherence_indicator', adherence=position.adherence)
            </div>
            % if system is None:
                <span class="non-desktop smaller-font">{{ position.system }}</span>
            % end
        </div>
    </td>
    % if system is None:
        <td class="desktop-only">{{ position.system }}</td>
    % end
    % if trip is None:
        <td class="lighter-text" colspan="4">Not in service</td>
    % else:
        % block = trip.block
        % stop = position.stop
        <td>
            <div class="flex-column">
                % include('components/headsign_indicator')
                <div class="mobile-only smaller-font">
                    Trip:
                    % include('components/trip_link', trip=trip, include_tooltip=False)
                </div>
                % if stop is not None:
                    <div class="non-desktop smaller-font">
                        Next Stop: <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                    </div>
                % end
            </div>
        </td>
        <td class="non-mobile">
            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
        </td>
        <td class="non-mobile">
            % include('components/trip_link', trip=trip)
        </td>
        <td class="desktop-only">
            % if stop is None:
                <span class="lighter-text">Unavailable</span>
            % else:
                <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
            % end
        </td>
    % end
</tr>
