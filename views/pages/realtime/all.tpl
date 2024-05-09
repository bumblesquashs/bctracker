
% rebase('base')

<div id="page-header">
    <h1>Realtime</h1>
    <h2>Currently active vehicles</h2>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section closed">
            <div class="header" onclick="toggleSection(this)">
                <h2>Options</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="column section">
                        <h3>Filters</h3>
                        <div class="options-container">
                            <div class="option" onclick="toggleNISBuses()">
                                <div id="show-nis-checkbox" class="checkbox {{ 'selected' if show_nis else '' }}">
                                    % include('components/svg', name='check')
                                </div>
                                <div>Show NIS Buses</div>
                            </div>
                        </div>
                    </div>
                    <div class="column section">
                        <h3>Sorting</h3>
                        <div class="options-container grid">
                            <div class="option" onclick="setSorting('bus_number')">
                                <div class="radio-button {{ 'selected' if sort_by == 'bus_number' else '' }}"></div>
                                <div>By Number</div>
                            </div>
                            <div class="option" onclick="setSorting('adherence')">
                                <div class="radio-button {{ 'selected' if sort_by == 'adherence' else '' }}"></div>
                                <div>By Adherence</div>
                            </div>
                            <div class="option" onclick="setSorting('speed')">
                                <div class="radio-button {{ 'selected' if sort_by == 'speed' else '' }}"></div>
                                <div>By Speed</div>
                            </div>
                        </div>
                    </div>
                    <div class="column section">
                        <h3>Grouping</h3>
                        <div class="options-container grid">
                            <div class="option" onclick="setGrouping('none')">
                                <div class="radio-button {{ 'selected' if group_by == 'none' else '' }}"></div>
                                <div>None</div>
                            </div>
                            <div class="option" onclick="setGrouping('model')">
                                <div class="radio-button {{ 'selected' if group_by == 'model' else '' }}"></div>
                                <div>By Model</div>
                            </div>
                            % if system:
                                <div class="option" onclick="setGrouping('route')">
                                    <div class="radio-button {{ 'selected' if group_by == 'route' else '' }}"></div>
                                    <div>By Route</div>
                                </div>
                            % end
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="section closed">
            <div class="header" onclick="toggleSection(this)">
                <h2>Statistics</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <table>
                    <thead>
                        <tr>
                            <th>Model</th>
                            % if show_nis:
                                <th class="no-wrap align-right">In Service</th>
                            % end
                            <th class="align-right">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        % models = sorted({p.bus.model for p in positions if p.bus.model is not None})
                        % model_types = sorted({m.type for m in models})
                        % for model_type in model_types:
                            % type_positions = [p for p in positions if p.bus.model is not None and p.bus.model.type == model_type]
                            <tr class="header">
                                <td>{{ model_type }}</td>
                                % if show_nis:
                                    <td class="align-right">{{ len([p for p in type_positions if p.trip is not None]) }}</td>
                                % end
                                <td class="align-right">{{ len(type_positions) }}</td>
                            </tr>
                            <tr class="display-none"></tr>
                            % type_models = [m for m in models if m.type == model_type]
                            % for model in type_models:
                                % model_positions = [p for p in type_positions if p.bus.model == model]
                                <tr>
                                    <td>{{! model }}</td>
                                    % if show_nis:
                                        <td class="align-right">{{ len([p for p in model_positions if p.trip is not None]) }}</td>
                                    % end
                                    <td class="align-right">{{ len(model_positions) }}</td>
                                </tr>
                            % end
                        % end
                        <tr class="header">
                            <td>Total</td>
                            % if show_nis:
                                <td class="align-right">{{ len([p for p in positions if p.trip is not None]) }}</td>
                            % end
                            <td class="align-right">{{ len(positions) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <script>
            function toggleNISBuses() {
                window.location = "{{ get_url(system, 'realtime', show_nis='false' if show_nis else 'true') }}"
            }
            
            function setSorting(sortBy) {
                window.location = "{{ get_url(system, 'realtime') }}?sort_by=" + sortBy;
            }
            
            function setGrouping(groupBy) {
                window.location = "{{ get_url(system, 'realtime') }}?group_by=" + groupBy;
            }
        </script>
    </div>
    <div class="container flex-3">
        % if len(positions) == 0:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>No Buses</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
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
                </div>
            </div>
        % else:
            % if group_by == 'model':
                % for model_type in model_types:
                    % type_models = [m for m in models if m.type == model_type]
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h2>{{ model_type }}</h2>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <div class="container">
                                % for model in type_models:
                                    % model_positions = sorted([p for p in positions if p.bus.model is not None and p.bus.model == model])
                                    % model_years = sorted({p.bus.order.year for p in model_positions})
                                    <div id="{{ model.id }}" class="section">
                                        <div class="header" onclick="toggleSection(this)">
                                            <h3>{{! model }}</h3>
                                            % include('components/toggle')
                                        </div>
                                        <div class="content">
                                            <table>
                                                <thead>
                                                    <tr>
                                                        <th>Bus</th>
                                                        % if system is None:
                                                            <th class="desktop-only">System</th>
                                                        % end
                                                        <th>Headsign</th>
                                                        <th class="non-mobile">Block</th>
                                                        <th class="non-mobile">Trip</th>
                                                        <th class="desktop-only">Next Stop</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    % for year in model_years:
                                                        % year_positions = [p for p in model_positions if p.bus.order.year == year]
                                                        <tr class="header">
                                                            <td colspan="7">
                                                                <div class="row space-between">
                                                                    <div>{{ year }}</div>
                                                                    <div>{{ len(year_positions) }}</div>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                        <tr class="display-none"></tr>
                                                        % for position in year_positions:
                                                            % include('rows/realtime', position=position)
                                                        % end
                                                    % end
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                % end
                            </div>
                        </div>
                    </div>
                % end
                
                % unknown_positions = sorted([p for p in positions if p.bus.order is None])
                % if len(unknown_positions) > 0:
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h2>Unknown Year/Model</h2>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Bus</th>
                                        % if system is None:
                                            <th class="desktop-only">System</th>
                                        % end
                                        <th>Headsign</th>
                                        <th class="non-mobile">Block</th>
                                        <th class="non-mobile">Trip</th>
                                        <th class="desktop-only">Next Stop</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % for position in unknown_positions:
                                        % include('rows/realtime', position=position)
                                    % end
                                </tbody>
                            </table>
                        </div>
                    </div>
                % end
            % elif system and group_by == 'route':
                % for route in system.get_routes():
                    % route_positions = [p for p in positions if p.trip is not None and p.trip.route == route]
                    % if len(route_positions) == 0:
                        % continue
                    % end
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <div class="column">
                                <h2 class="row">
                                    % include('components/route')
                                    <div>{{! route.display_name }}</div>
                                </h2>
                                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">View schedule and details</a>
                            </div>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Bus</th>
                                        <th class="desktop-only">Model</th>
                                        % if system is None:
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
                                        % if last_bus is None:
                                            % same_order = True
                                        % elif order is None and last_bus.order is None:
                                            % same_order = True
                                        % elif order is None or last_bus.order is None:
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
                                                        % include('components/adherence', adherence=position.adherence)
                                                    </div>
                                                    <span class="non-desktop smaller-font">
                                                        % include('components/order')
                                                    </span>
                                                </div>
                                            </td>
                                            <td class="desktop-only">
                                                % include('components/order')
                                            </td>
                                            % if system is None:
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
                                                    % if stop is not None:
                                                        <div class="non-desktop smaller-font">
                                                            Next Stop: <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                                        </div>
                                                    % end
                                                </div>
                                            </td>
                                            <td class="non-mobile">
                                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                            </td>
                                            <td class="non-mobile">
                                                % include('components/trip')
                                            </td>
                                            <td class="desktop-only">
                                                % if stop is None:
                                                    <span class="lighter-text">Unavailable</span>
                                                % else:
                                                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                                % end
                                            </td>
                                        </tr>
                                    % end
                                </tbody>
                            </table>
                        </div>
                    </div>
                % end
                
                % no_route_positions = sorted([p for p in positions if p.trip is None])
                % if len(no_route_positions) > 0:
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
                                        % if system is None:
                                            <th>System</th>
                                        % end
                                    </tr>
                                </thead>
                                <tbody>
                                    % last_bus = None
                                    % for position in no_route_positions:
                                        % bus = position.bus
                                        % order = bus.order
                                        % if last_bus is None:
                                            % same_order = True
                                        % elif order is None and last_bus.order is None:
                                            % same_order = True
                                        % elif order is None or last_bus.order is None:
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
                                            % if system is None:
                                                <td>{{ position.system }}</td>
                                            % end
                                        </tr>
                                    % end
                                </tbody>
                            </table>
                        </div>
                    </div>
                % end
            % else:
                <div class="section">
                    <div class="header" onclick="toggleSection(this)">
                        <h2>All Buses</h2>
                        % include('components/toggle')
                    </div>
                    <div class="content">
                        % known_positions = [p for p in positions if p.bus.order is not None]
                        % orders = sorted({p.bus.order for p in known_positions})
                        % unknown_positions = sorted([p for p in positions if p.bus.order is None])
                        <table>
                            <thead>
                                <tr>
                                    <th>Bus</th>
                                    % if system is None:
                                        <th class="desktop-only">System</th>
                                    % end
                                    <th>Headsign</th>
                                    <th class="non-mobile">Block</th>
                                    <th class="non-mobile">Trip</th>
                                    <th class="desktop-only">Next Stop</th>
                                </tr>
                            </thead>
                            <tbody>
                                % if len(unknown_positions) > 0:
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
                    </div>
                </div>
            % end
                
            % include('components/top_button')
        % end
    </div>
</div>
