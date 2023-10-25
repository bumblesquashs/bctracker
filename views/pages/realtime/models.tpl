
% rebase('base')

<div class="page-header">
    <h1 class="title">Realtime</h1>
    <h2 class="subtitle">Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'realtime') }}" class="tab-button">All Buses</a>
        % if system is not None:
            <a href="{{ get_url(system, 'realtime/routes') }}" class="tab-button">By Route</a>
        % end
        <span class="tab-button current">By Model</span>
        % if show_speed:
            <a href="{{ get_url(system, 'realtime/speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Keanu Reeves and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
</div>

% if len(positions) == 0:
    <div class="placeholder">
        % if system is None:
            <h3 class="title">There are no buses out right now</h3>
            <p>
                BC Transit does not have late night service, so this should be the case overnight.
                If you look out your window and the sun is shining, there may be an issue getting up-to-date info.
            </p>
            <p>Please check again later!</p>
        % elif not system.realtime_enabled:
            <h3 class="title">{{ system }} does not support realtime</h3>
            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % elif not system.is_loaded:
            <h3 class="title">Realtime information for {{ system }} is unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % else:
            <h3 class="title">There are no buses out in {{ system }} right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% else:
    % models = sorted({p.bus.model for p in positions if p.bus.model is not None})
    % model_types = sorted({m.type for m in models})
    <div class="flex-container">
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header">
                    <h2>Statistics</h2>
                </div>
                <div class="content">
                    <table class="striped">
                        <thead>
                            <tr>
                                <th>Model</th>
                                <th class="no-wrap">In Service</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for type in model_types:
                                % type_positions = [p for p in positions if p.bus.model is not None and p.bus.model.type == type]
                                <tr class="section">
                                    <td>{{ type }}</td>
                                    <td>{{ len([p for p in type_positions if p.trip is not None]) }}</td>
                                    <td>{{ len(type_positions) }}</td>
                                </tr>
                                <tr class="display-none"></tr>
                                % type_models = [m for m in models if m.type == type]
                                % for model in type_models:
                                    % model_positions = [p for p in type_positions if p.bus.model == model]
                                    <tr>
                                        <td><a href="#{{ model.id }}">{{! model }}</a></td>
                                        <td>{{ len([p for p in model_positions if p.trip is not None]) }}</td>
                                        <td>{{ len(model_positions) }}</td>
                                    </tr>
                                % end
                            % end
                            <tr class="section">
                                <td>Total</td>
                                <td>{{ len([p for p in positions if p.trip is not None]) }}</td>
                                <td>{{ len(positions) }}</td>
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
                    <div class="header">
                        <h2>{{ type }}</h2>
                    </div>
                    <div class="content">
                        <div class="container">
                            % for model in type_models:
                                % model_positions = sorted([p for p in positions if p.bus.model is not None and p.bus.model == model])
                                % model_years = sorted({p.bus.order.year for p in model_positions})
                                <div id="{{ model.id }}" class="section">
                                    <div class="header">
                                        <h3>{{! model }}</h3>
                                    </div>
                                    <div class="content">
                                        <table class="striped">
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
                                                    <tr class="section">
                                                        <td colspan="7">
                                                            <div class="flex-row">
                                                                <div class="flex-1">{{ year }}</div>
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
                    <div class="header">
                        <h2>Unknown Year/Model</h2>
                    </div>
                    <div class="content">
                        <table class="striped">
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
        </div>
    </div>
% end

% include('components/top_button')
