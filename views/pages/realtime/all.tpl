
% rebase('base', title='Realtime')

<div class="page-header">
    <h1 class="title">Realtime</h1>
    <h2 class="subtitle">Currently active vehicles</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">All Buses</span>
        % if system is not None:
            <a href="{{ get_url(system, 'realtime/routes') }}" class="tab-button">By Route</a>
        % end
        <a href="{{ get_url(system, 'realtime/models') }}" class="tab-button">By Model</a>
        % if show_speed:
            <a href="{{ get_url(system, 'realtime/speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Sandra Bullock and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
    <hr />
</div>

% if len(positions) == 0:
    <div>
        % if system is not None and not system.realtime_enabled:
            <p>
                {{ system }} does not currently support realtime.
                You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
            </p>
        % else:
            % if system is None:
                There are no buses out right now.
                BC Transit does not have late night service, so this should be the case overnight.
                If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.
                Please check back later!
            % else:
                <p>
                    There are no buses out in {{ system }} right now.
                    Please choose a different system.
                </p>
            % end
        % end
    </div>
% else:
    % known_positions = [p for p in positions if p.bus.order is not None]
    % orders = sorted({p.bus.order for p in known_positions})
    % unknown_positions = sorted([p for p in positions if p.bus.order is None])
    <table class="striped">
        <thead>
            <tr>
                <th>Bus</th>
                % if system is None:
                    <th class="non-mobile">System</th>
                % end
                <th class="desktop-only">Headsign</th>
                <th class="desktop-only">Block</th>
                <th class="desktop-only">Trip</th>
                <th class="desktop-only">Current Stop</th>
                <th class="non-desktop">Details</th>
            </tr>
        </thead>
        <tbody>
            % if len(unknown_positions) > 0:
                <tr class="section">
                    <td colspan="7">
                        <div class="flex-row">
                            <div class="flex-1">Unknown Year/Model</div>
                            <div>{{ len(unknown_positions) }}</div>
                        </div>
                    </td>
                </tr>
                <tr class="display-none"></tr>
                % for position in unknown_positions:
                    % include('rows/realtime', position=position)
                % end
            % end
            % for order in orders:
                % order_positions = sorted([p for p in known_positions if p.bus.order == order])
                <tr class="section">
                    <td colspan="7">
                        <div class="flex-row">
                            <div class="flex-1">{{ order }}</div>
                            <div>{{ len(order_positions) }}</div>
                        </div>
                    </td>
                </tr>
                <tr class="display-none"></tr>
                % for position in order_positions:
                    % include('rows/realtime', position=position)
                % end
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
