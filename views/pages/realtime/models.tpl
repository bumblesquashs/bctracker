
% rebase('base')

<div id="page-header">
    <h1>Realtime</h1>
    <h2>Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'realtime') }}" class="tab-button">All Buses</a>
        % if context.system:
            <a href="{{ get_url(context, 'realtime', 'routes') }}" class="tab-button">By Route</a>
        % end
        <span class="tab-button current">By Model</span>
        % if show_speed:
            <a href="{{ get_url(context, 'realtime', 'speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Keanu Reeves and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
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
    % models = sorted({p.bus.model for p in positions if p.bus.model})
    % model_types = sorted({m.type for m in models})
    <div class="page-container">
        <div class="sidebar container flex-1">
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
                            % for type in model_types:
                                % type_positions = [p for p in positions if p.bus.model and p.bus.model.type == type]
                                <tr class="header">
                                    <td>{{ type }}</td>
                                    % if show_nis:
                                        <td class="align-right">{{ len([p for p in type_positions if p.trip]) }}</td>
                                    % end
                                    <td class="align-right">{{ len(type_positions) }}</td>
                                </tr>
                                <tr class="display-none"></tr>
                                % type_models = [m for m in models if m.type == type]
                                % for model in type_models:
                                    % model_positions = [p for p in type_positions if p.bus.model == model]
                                    <tr>
                                        <td><a href="#{{ model.id }}">{{! model }}</a></td>
                                        % if show_nis:
                                            <td class="align-right">{{ len([p for p in model_positions if p.trip]) }}</td>
                                        % end
                                        <td class="align-right">{{ len(model_positions) }}</td>
                                    </tr>
                                % end
                            % end
                            <tr class="header">
                                <td>Total</td>
                                % if show_nis:
                                    <td class="align-right">{{ len([p for p in positions if p.trip]) }}</td>
                                % end
                                <td class="align-right">{{ len(positions) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="container flex-3">
            % for type in model_types:
                % type_models = [m for m in models if m.type == type]
                <div class="section">
                    <div class="header" onclick="toggleSection(this)">
                        <h2>{{ type }}</h2>
                        % include('components/toggle')
                    </div>
                    <div class="content">
                        <div class="container">
                            % for model in type_models:
                                % model_positions = sorted([p for p in positions if p.bus.model and p.bus.model == model])
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
            
            % unknown_positions = sorted([p for p in positions if not p.bus.order])
            % if unknown_positions:
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
                                % for position in unknown_positions:
                                    % include('rows/realtime', position=position)
                                % end
                            </tbody>
                        </table>
                    </div>
                </div>
            % end
        </div>
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
        window.location = "{{ get_url(context, 'realtime', 'models', show_nis='false' if show_nis else 'true') }}"
    }
</script>
