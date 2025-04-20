
% rebase('base')

<div id="page-header">
    <h1>Realtime</h1>
    <h2>Currently active vehicles</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">All Buses</span>
        % if context.system:
            <a href="{{ get_url(context, 'realtime', 'routes') }}" class="tab-button">By Route</a>
        % end
        <a href="{{ get_url(context, 'realtime', 'models') }}" class="tab-button">By Model</a>
        % if show_speed:
            <a href="{{ get_url(context, 'realtime', 'speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Sandra Bullock and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
</div>

<div class="options-container">
    <div class="option" onclick="toggleNISBuses()">
        <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
            % include('components/svg', name='status/check')
        </div>
        <div>Show NIS Buses</div>
    </div>
</div>

% if positions:
    % known_positions = [p for p in positions if p.bus.order]
    % orders = sorted({p.bus.order for p in known_positions})
    % unknown_positions = sorted([p for p in positions if not p.bus.order])
    <table>
        <thead>
            <tr>
                <th>Bus</th>
                % if not context.system:
                    <th class="desktop-only">System</th>
                % end
                <th>Headsign</th>
                <th class="non-mobile">Block</th>
                <th class="non-mobile">Trip</th>
                <th class="desktop-only">Next Stop</th>
            </tr>
        </thead>
        <tbody>
            % if unknown_positions:
                <tr class="header">
                    <td colspan="6">
                        <div class="row space-between">
                            <div>Unknown Year/Model</div>
                            <div>{{ len(unknown_positions) }}</div>
                        </div>
                    </td>
                </tr>
                <tr class="display-none"></tr>
                % for position in unknown_positions:
                    % include('rows/realtime')
                % end
            % end
            % for order in orders:
                % order_positions = sorted([p for p in known_positions if p.bus.order == order])
                <tr class="header">
                    <td colspan="6">
                        <div class="row space-between">
                            <div>{{! order }}</div>
                            <div>{{ len(order_positions) }}</div>
                        </div>
                    </td>
                </tr>
                <tr class="display-none"></tr>
                % for position in order_positions:
                    % include('rows/realtime')
                % end
            % end
        </tbody>
    </table>
    
    % include('components/top_button')
% else:
    <div class="placeholder">
        % if not context.system:
            % if show_nis:
                <h3>There are no buses out right now</h3>
                <p>
                    None of our current agencies operate late night service, so this should be the case overnight.
                    If you look out your window and the sun is shining, there may be an issue getting up-to-date info.
                </p>
                <p>Please check again later!</p>
            % else:
                <h3>There are no buses in service right now</h3>
                <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
            % end
        % elif not context.realtime_enabled:
            <h3>{{ context.system }} realtime information is not supported</h3>
            <p>You can browse schedule data for using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % elif not context.system.realtime_loaded:
            <h3>{{ context.system }} realtime information is unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % elif not show_nis:
            <h3>There are no {{ context.system }} buses in service right now</h3>
            <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
        % else:
            <h3>There are no {{ context.system }} buses out right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% end

<script>
    function toggleNISBuses() {
        window.location = "{{ get_url(context, 'realtime', show_nis='false' if show_nis else 'true') }}"
    }
</script>
