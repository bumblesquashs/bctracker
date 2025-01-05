
% bus = position.bus
% trip = position.trip

<tr>
    <td>
        <div class="column">
            <div class="row">
                % include('components/bus')
                <div class="row gap-5">
                    % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                    % include('components/adherence', adherence=position.adherence)
                </div>
            </div>
            % if not system:
                <span class="non-desktop smaller-font">{{ position.system }}</span>
            % end
        </div>
    </td>
    % if not system:
        <td class="desktop-only">{{ position.system }}</td>
    % end
    % if trip:
        % block = trip.block
        % stop = position.stop
        <td>
            <div class="column">
                % include('components/headsign')
                <div class="mobile-only smaller-font">
                    Trip:
                    % include('components/trip', include_tooltip=False)
                </div>
                % if stop:
                    <div class="non-desktop smaller-font">
                        <span class="align-middle">Next Stop:</span>
                        % include('components/stop')
                    </div>
                % end
            </div>
        </td>
        <td class="non-mobile">
            <a href="{{ get_url(block.system, 'blocks', block) }}">{{ block.id }}</a>
        </td>
        <td class="non-mobile">
            % include('components/trip')
        </td>
        <td class="desktop-only">
            % include('components/stop')
        </td>
    % else:
        <td class="lighter-text" colspan="4">Not in service</td>
    % end
</tr>
