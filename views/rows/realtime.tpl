
% bus = position.bus
% trip = position.trip

<tr>
    <td>
        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
        % if system is None:
            <br class="mobile-only" />
            <span class="mobile-only smaller-font">{{ position.system }}</span>
        % end
    </td>
    % if system is None:
        <td class="non-mobile">{{ position.system }}</td>
    % end
    % if trip is None:
        <td class="lighter-text" colspan="4">Not in service</td>
    % else:
        % block = trip.block
        % stop = position.stop
        <td class="desktop-only">{{ trip }}</td>
        <td class="non-mobile">
            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
        </td>
        <td>
            <div class="flex-row">
                % if stop is not None:
                    <div class="non-desktop">
                        % include('components/adherence_indicator', adherence=position.adherence)
                    </div>
                % end
                <div class="flex-1">
                    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
                    <br class="non-desktop" />
                    <span class="non-desktop smaller-font">{{ trip }}</span>
                </div>
            </div>
        </td>
        % if stop is None:
            <td class="desktop-only lighter-text">Unavailable</td>
        % else:
            <td class="desktop-only">
                <div class="flex-row">
                    % include('components/adherence_indicator', adherence=position.adherence)
                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}" class="flex-1">{{ stop }}</a>
                </div>
            </td>
        % end
    % end
</tr>
