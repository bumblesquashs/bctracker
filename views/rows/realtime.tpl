
% bus = position.bus

<tr>
    <td><a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a></td>
    % if system is None:
        <td class="non-mobile">{{ position.system }}</td>
    % end
    % if position.trip is None:
        <td class="lighter-text">Not in service</td>
        <td class="desktop-only"></td>
        <td class="desktop-only"></td>
        <td class="desktop-only"></td>
    % else:
        % trip = position.trip
        % block = position.trip.block
        % stop = position.stop
        <td>
            {{ trip }}
            % if stop is not None:
                <br class="non-desktop" />
                <span class="non-desktop smaller-font">
                    % include('components/adherence_indicator', adherence=position.adherence)
                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                </span>
            % end
        </td>
        <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
        <td class="desktop-only"><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a></td>
        % if stop is None:
            <td class="desktop-only lighter-text">Unavailable</td>
        % else:
            <td class="desktop-only">
                % include('components/adherence_indicator', adherence=position.adherence)
                <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
            </td>
        % end
    % end
</tr>