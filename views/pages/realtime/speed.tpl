
% rebase('base')

<div id="page-header">
    <h1>Realtime</h1>
    <h2>Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, agency, '/realtime') }}" class="tab-button">All Buses</a>
        % if system is not None:
            <a href="{{ get_url(system, agency, '/realtime/routes') }}" class="tab-button">By Route</a>
        % end
        <a href="{{ get_url(system, agency, '/realtime/models') }}" class="tab-button">By Model</a>
        <span class="tab-button current">By Speed</span>
    </div>
</div>

<div class="checkbox-container" onclick="toggleNISBuses()">
    <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
        <img class="white" src="/img/white/check.png" />
        <img class="black" src="/img/black/check.png" />
    </div>
    <div>Show NIS Buses</div>
</div>

% if len(positions) == 0:
    <div class="placeholder">
        % if system is None:
            % if show_nis:
                <h3>There are no buses out right now</h3>
                <p>
                    BC Transit does not have late night service, so this should be the case overnight.
                    If you look out your window and the sun is shining, there may be an issue getting up-to-date info.
                </p>
                <p>Please check again later!</p>
            % else:
                <h3>There are no buses in service right now</h3>
                <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
            % end
        % elif not system.realtime_enabled:
            <h3>{{ system }} does not support realtime</h3>
            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % elif not system.realtime_loaded:
            <h3>Realtime information for {{ system }} is unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % elif not show_nis:
            <h3>There are no buses in service in {{ system }} right now</h3>
            <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
        % else:
            <h3>There are no buses out in {{ system }} right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% else:
    <table>
        <thead>
            <tr>
                <th>Bus</th>
                <th class="desktop-only">Model</th>
                % if system is None:
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
                % same_speed = last_speed is None or position.speed // 10 == last_speed
                % last_speed = position.speed // 10
                <tr class="{{'' if same_speed else 'divider'}}">
                    <td>
                        <div class="column">
                            <div class="row">
                                % include('components/bus')
                                % include('components/adherence', adherence=position.adherence)
                            </div>
                            <span class="non-desktop smaller-font">
                                % include('components/order', order=bus.order)
                            </span>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % include('components/order', order=bus.order)
                    </td>
                    % if system is None:
                        <td class="desktop-only">{{ position.system }}</td>
                    % end
                    <td class="desktop-only no-wrap">{{ position.speed }} km/h</td>
                    % if position.trip is None:
                        <td colspan="4">
                            <div class="column">
                                <span class="lighter-text">Not in service</span>
                                <span class="non-desktop smaller-font no-wrap">{{ position.speed }} km/h</span>
                            </div>
                        </td>
                    % else:
                        % trip = position.trip
                        % block = trip.block
                        % stop = position.stop
                        <td>
                            <div class="column">
                                % include('components/headsign')
                                <span class="non-desktop smaller-font no-wrap">{{ position.speed }} km/h</span>
                                <div class="mobile-only smaller-font">
                                    Trip:
                                    % include('components/trip')
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
                                <a href="{{ get_url(stop.system, block.agency, f'/stops/{stop.number}') }}">{{ stop }}</a>
                            % end
                        </td>
                    % end
                </tr>
            % end
        </tbody>
    </table>
    
    % include('components/top_button')
% end

<script>
    function toggleNISBuses() {
        window.location = "{{ get_url(system, agency, '/realtime/speed', show_nis='false' if show_nis else 'true') }}"
    }
</script>
