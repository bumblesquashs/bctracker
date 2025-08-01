
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
    <div class="table-border-wrapper">
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
                    % if context.enable_blocks:
                        <th class="non-mobile">Block</th>
                    % end
                    <th class="non-mobile">Trip</th>
                    <th class="desktop-only">Next Stop</th>
                </tr>
            </thead>
            <tbody>
                % last_speed = None
                % for position in sorted(positions, key=lambda p: p.speed, reverse=True):
                    % bus = position.bus
                    % trip = position.trip
                    % stop = position.stop
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
                                    % include('components/year_model', year_model=bus.year_model)
                                </span>
                            </div>
                        </td>
                        <td class="desktop-only">
                            % include('components/year_model', year_model=bus.year_model)
                        </td>
                        % if not context.system:
                            <td class="desktop-only">{{ position.context }}</td>
                        % end
                        <td class="desktop-only no-wrap">{{ position.speed }} km/h</td>
                        % if trip:
                            % block = trip.block
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
                            % if context.enable_blocks:
                                <td class="non-mobile">
                                    <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                </td>
                            % end
                            <td class="non-mobile">
                                % include('components/trip')
                            </td>
                        % else:
                            <td colspan="3">
                                <div class="column">
                                    <span class="lighter-text">Not In Service</span>
                                    <span class="non-desktop smaller-font no-wrap">{{ position.speed }} km/h</span>
                                    % if stop:
                                        <div class="non-desktop smaller-font">
                                            <span class="align-middle">Next Stop:</span>
                                            % include('components/stop')
                                        </div>
                                    % end
                                </div>
                            </td>
                        % end
                        <td class="desktop-only">
                            % include('components/stop')
                        </td>
                    </tr>
                % end
            </tbody>
        </table>
    </div>
    
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
            <h3>{{ context }} realtime information is not supported</h3>
            <p>You can browse schedule data using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % elif not context.realtime_loaded:
            <h3>{{ context }} realtime information is unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % elif not show_nis:
            <h3>There are no {{ context }} buses in service right now</h3>
            <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
        % else:
            <h3>There are no {{ context }} buses out right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% end

<script>
    function toggleNISBuses() {
        window.location = "{{ get_url(context, 'realtime', 'speed', show_nis='false' if show_nis else 'true') }}"
    }
</script>
