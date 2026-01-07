
% rebase('base')

<div id="page-header">
    <h1>Realtime</h1>
    <h2>Currently active {{ context.vehicle_type_plural.lower() }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'realtime') }}" class="tab-button">All {{ context.vehicle_type_plural }}</a>
        <span class="tab-button current">By Route</span>
        <a href="{{ get_url(context, 'realtime', 'models') }}" class="tab-button">By Model</a>
        % if show_speed:
            <a href="{{ get_url(context, 'realtime', 'speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Dennis Hopper and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
</div>

<div class="options-container">
    <div class="option" onclick="toggleNISVehicles()">
        <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
            % include('components/svg', name='status/check')
        </div>
        <div>Show NIS {{ context.vehicle_type_plural }}</div>
    </div>
</div>

% if context.system and positions:
    <div class="container">
        % for route in context.system.get_routes():
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
                        <a href="{{ get_url(route.context, 'routes', route) }}">View schedule and details</a>
                    </div>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>{{ context.vehicle_type }}</th>
                                <th class="desktop-only">Model</th>
                                % if not context.system:
                                    <th class="desktop-only">System</th>
                                % end
                                <th>Headsign</th>
                                % if context.enable_blocks:
                                    <th class="non-mobile">Block</th>
                                % end
                                <th class="non-mobile">Trip</th>
                                <th class="desktop-only">Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_vehicle = None
                            % for position in sorted(route_positions):
                                % vehicle = position.vehicle
                                % order_id = vehicle.order_id
                                % if not last_vehicle:
                                    % same_order = True
                                % elif not order_id and not last_vehicle.order_id:
                                    % same_order = True
                                % elif not order_id or not last_vehicle.order_id:
                                    % same_order = False
                                % else:
                                    % same_order = order_id == last_vehicle.order_id
                                % end
                                % last_vehicle = vehicle
                                <tr class="{{'' if same_order else 'divider'}}">
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % include('components/vehicle')
                                                <div class="row gap-5">
                                                    % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                    % include('components/adherence', adherence=position.adherence)
                                                </div>
                                            </div>
                                            <span class="non-desktop smaller-font">
                                                % include('components/year_model', year_model=vehicle.year_model)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/year_model', year_model=vehicle.year_model)
                                    </td>
                                    % if not context.system:
                                        <td class="desktop-only">{{ position.context }}</td>
                                    % end
                                    % trip = position.trip
                                    % block = trip.block
                                    % stop = position.stop
                                    <td>
                                        <div class="column">
                                            % include('components/headsign', departure=position.departure)
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
                                    % if context.enable_blocks:
                                        <td class="non-mobile">
                                            <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                        </td>
                                    % end
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
                    <table>
                        <thead>
                            <tr>
                                <th>{{ context.vehicle_type }}</th>
                                <th class="desktop-only">Model</th>
                                % if not context.system:
                                    <th>System</th>
                                % end
                                <th>Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_vehicle = None
                            % for position in no_route_positions:
                                % vehicle = position.vehicle
                                % stop = position.stop
                                % order_id = vehicle.order_id
                                % if not last_vehicle:
                                    % same_order = True
                                % elif not order_id and not last_vehicle.order_id:
                                    % same_order = True
                                % elif not order_id or not last_vehicle.order_id:
                                    % same_order = False
                                % else:
                                    % same_order = order_id == last_vehicle.order_id
                                % end
                                % last_vehicle = vehicle
                                <tr class="{{'' if same_order else 'divider'}}">
                                    <td>
                                        <div class="column">
                                            % include('components/vehicle')
                                            <span class="non-desktop smaller-font">
                                                % include('components/year_model', year_model=vehicle.year_model)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/year_model', year_model=vehicle.year_model)
                                    </td>
                                    % if not context.system:
                                        <td>{{ position.context }}</td>
                                    % end
                                    <td>
                                        % include('components/stop')
                                    </td>
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
        % if not context.system:
            <h3>Realtime routes can only be viewed for individual systems.</h3>
            <p>Please choose a system.</p>
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
            <h3>There are no {{ context }} {{ context.vehicle_type_plural.lower() }} in service right now</h3>
            <p>You can see all active {{ context.vehicle_type_plural.lower() }}, including ones not in service, by selecting the <b>Show NIS {{ context.vehicle_type_plural }}</b> checkbox.</p>
        % else:
            <h3>There are no {{ context }} {{ context.vehicle_type_plural.lower() }} out right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% end

<script>
    function toggleNISVehicles() {
        window.location = "{{ get_url(context, 'realtime', 'routes', show_nis='false' if show_nis else 'true') }}"
    }
</script>
