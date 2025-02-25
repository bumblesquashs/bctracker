
% rebase('base')

<div id="page-header">
    <h1>Realtime</h1>
    <h2>Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'realtime') }}" class="tab-button">All Buses</a>
        <span class="tab-button current">By Route</span>
        <a href="{{ get_url(system, 'realtime', 'models') }}" class="tab-button">By Model</a>
        % if show_speed:
            <a href="{{ get_url(system, 'realtime', 'speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Dennis Hopper and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
</div>

<div class="options-container">
    <div class="option" onclick="toggleNISBuses()">
        <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
            % include('components/svg', name='check')
        </div>
        <div>Show NIS Buses</div>
    </div>
</div>

% if positions:
    <div class="container">
        % for route in system.get_routes():
            % route_positions = [p for p in positions if p.trip and p.trip.route == route]
            % if not route_positions:
                % continue
            % end
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <div class="column">
                        <h2 class="row">
                            % include('components/route')
                            <div>{{! route.display_name }}</div>
                        </h2>
                        <a href="{{ get_url(route.system, 'routes', route) }}">View schedule and details</a>
                    </div>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="desktop-only">Model</th>
                                % if not system:
                                    <th class="desktop-only">System</th>
                                % end
                                <th>Headsign</th>
                                <th class="non-mobile">Block</th>
                                <th class="non-mobile">Trip</th>
                                <th class="desktop-only">Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_bus = None
                            % for position in sorted(route_positions):
                                % bus = position.bus
                                % order = bus.order
                                % if not last_bus:
                                    % same_order = True
                                % elif not order and not last_bus.order:
                                    % same_order = True
                                % elif not order or not last_bus.order:
                                    % same_order = False
                                % else:
                                    % same_order = order == last_bus.order
                                % end
                                % last_bus = bus
                                <tr class="{{'' if same_order else 'divider'}}">
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
                                                % include('components/order')
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/order')
                                    </td>
                                    % if not system:
                                        <td class="desktop-only">{{ position.system }}</td>
                                    % end
                                    % trip = position.trip
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
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
        
        % no_route_positions = sorted([p for p in positions if not p.trip])
        % if no_route_positions:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Not In Service</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table class="striped">
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="desktop-only">Model</th>
                                % if not system:
                                    <th>System</th>
                                % end
                            </tr>
                        </thead>
                        <tbody>
                            % last_bus = None
                            % for position in no_route_positions:
                                % bus = position.bus
                                % order = bus.order
                                % if not last_bus:
                                    % same_order = True
                                % elif not order and not last_bus.order:
                                    % same_order = True
                                % elif not order or not last_bus.order:
                                    % same_order = False
                                % else:
                                    % same_order = order == last_bus.order
                                % end
                                % last_bus = bus
                                <tr class="{{'' if same_order else 'divider'}}">
                                    <td>
                                        <div class="column">
                                            % include('components/bus')
                                            <span class="non-desktop smaller-font">
                                                % include('components/order')
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/order')
                                    </td>
                                    % if not system:
                                        <td>{{ position.system }}</td>
                                    % end
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
    </div>
    
    % include('components/top_button')
% else:
    <div class="placeholder">
        % if not system:
            <h3>Realtime routes can only be viewed for individual systems.</h3>
            <p>
                None of our current agencies operate late night service, so this should be the case overnight.
                If you look out your window and the sun is shining, there may be an issue getting up-to-date info.
            </p>
            <p>Please choose a system.</p>
        % elif not system.realtime_enabled:
            <h3>{{ system }} realtime information is not supported</h3>
            <p>You can browse schedule data for using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % elif not system.realtime_loaded:
            <h3>{{ system }} realtime information is unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % elif not show_nis:
            <h3>There are no {{ system }} buses in service right now</h3>
            <p>You can see all active buses, including ones not in service, by selecting the <b>Show NIS Buses</b> checkbox.</p>
        % else:
            <h3>There are no {{ system }} buses out right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% end

<script>
    function toggleNISBuses() {
        window.location = "{{ get_url(system, 'realtime', 'routes', show_nis='false' if show_nis else 'true') }}"
    }
</script>
