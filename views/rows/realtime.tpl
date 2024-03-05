
% bus = position.bus
% trip = position.trip

<tr>
    <td>
        <div class="column">
            <div class="row">
                % include('components/bus')
                % include('components/adherence', adherence=position.adherence)
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
            <div class="column">
                % include('components/headsign')
                <div class="mobile-only smaller-font">
                    Trip:
                    % include('components/trip', include_tooltip=False)
                </div>
                % if stop is not None:
                    <div class="non-desktop smaller-font">
                        Next Stop: <a href="{{ get_url(stop.system, stop.agency, f'/stops/{stop.number}') }}">{{ stop }}</a>
                    </div>
                % end
            </div>
        </td>
        <td class="non-mobile">
            <a href="{{ get_url(block.system, block.agency, f'/blocks/{block.id}') }}">{{ block.id }}</a>
        </td>
        <td class="non-mobile">
            % include('components/trip')
        </td>
        <td class="desktop-only">
            % if stop is None:
                <span class="lighter-text">Unavailable</span>
            % else:
                <a href="{{ get_url(stop.system, stop.agency, f'/stops/{stop.number}') }}">{{ stop }}</a>
            % end
        </td>
    % end
</tr>
