
% rebase('base')

<div id="page-header">
    <h1>Realtime</h1>
    <h2>Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'realtime') }}" class="tab-button">All Buses</a>
        % if context.system:
            <a href="{{ get_url(context, 'realtime', 'routes') }}" class="tab-button">By Route</a>
        % end
        <a href="{{ get_url(context, 'realtime', 'models') }}" class="tab-button">By Model</a>
        <span class="tab-button current">By Speed</span>
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
    <table>
        <thead>
            <tr>
                <th>Bus</th>
                <th class="desktop-only">Model</th>
                % if not context.system:
                    <th class="desktop-only">System</th>
                % end
                <th class="desktop-only">Speed</th>
                <th>Headsign</th>
                <th class="non-mobile">Block</th>
                <th class="non-mobile">Trip</th>
                <th class="desktop-only">Next Stop</th>
            </tr>
        </thead>
        <tbody>
            % last_speed = None
            % for position in sorted(positions, key=lambda p: p.speed, reverse=True):
                % bus = position.bus
                % same_speed = not last_speed or position.speed // 10 == last_speed
                % last_speed = position.speed // 10
                <tr class="{{'' if same_speed else 'divider'}}">
                    <td>
                        <div class="column">
                            <div class="row">
                                % include('components/bus')
                                <div class="row gap-5">
                                    % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                    % include('components/adherence', adherence=position.adherence)
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
                    % if not context.system:
                        <td class="desktop-only">{{ position.system }}</td>
                    % end
                    <td class="desktop-only no-wrap">{{ position.speed }} km/h</td>
                    % if position.trip:
                        % trip = position.trip
                        % block = trip.block
                        % stop = position.stop
                        <td>
                            <div class="column">
                                % include('components/headsign', departure=position.departure)
                                <span class="non-desktop smaller-font no-wrap">{{ position.speed }} km/h</span>
                                <div class="mobile-only smaller-font">
                                    Trip:
                                    % include('components/trip')
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
                        <td colspan="4">
                            <div class="column">
                                <span class="lighter-text">Not in service</span>
                                <span class="non-desktop smaller-font no-wrap">{{ position.speed }} km/h</span>
                            </div>
                        </td>
                    % end
                </tr>
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
        window.location = "{{ get_url(context, 'realtime', 'speed', show_nis='false' if show_nis else 'true') }}"
    }
</script>
