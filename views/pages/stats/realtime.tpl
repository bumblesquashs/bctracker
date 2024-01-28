
% rebase('base')

<div id="page-header">
    <h1>Statistics</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'stats') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Realtime</span>
        <a href="{{ get_url(system, 'stats/history') }}" class="tab-button">History</a>
    </div>
</div>

% if len(positions) == 0:
    <div class="placeholder">
        % if system is None:
            <h3>There are no buses out right now</h3>
            <p>
                BC Transit does not have late night service, so this should be the case overnight.
                If you look out your window and the sun is shining, there may be an issue getting up-to-date info.
            </p>
            <p>Please check again later!</p>
        % elif not system.realtime_enabled:
            <h3>{{ system }} does not support realtime</h3>
            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % elif not system.is_loaded:
            <h3>Realtime information for {{ system }} is unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % else:
            <h3>There are no buses out in {{ system }} right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% else:
    % models = sorted({p.bus.model for p in positions if p.bus.model is not None})
    % model_types = sorted({m.type for m in models})
    
    <table>
        <thead>
            <tr>
                <th>Model</th>
                <th>In Service</th>
                <th>Not In Service</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            % for type in model_types:
                % type_positions = [p for p in positions if p.bus.model is not None and p.bus.model.type == type]
                <tr class="header">
                    <td>{{ type }}</td>
                    <td>{{ len([p for p in type_positions if p.trip is not None]) }}</td>
                    <td>{{ len([p for p in type_positions if p.trip is None]) }}</td>
                    <td>{{ len(type_positions) }}</td>
                </tr>
                <tr class="display-none"></tr>
                % type_models = [m for m in models if m.type == type]
                % for model in type_models:
                    % model_positions = [p for p in type_positions if p.bus.model == model]
                    <tr>
                        <td>{{! model }}</td>
                        <td>{{ len([p for p in model_positions if p.trip is not None]) }}</td>
                        <td>{{ len([p for p in model_positions if p.trip is None]) }}</td>
                        <td>{{ len(model_positions) }}</td>
                    </tr>
                % end
            % end
            <tr class="header">
                <td>Total</td>
                <td>{{ len([p for p in positions if p.trip is not None]) }}</td>
                <td>{{ len([p for p in positions if p.trip is None]) }}</td>
                <td>{{ len(positions) }}</td>
            </tr>
        </tbody>
    </table>
% end
