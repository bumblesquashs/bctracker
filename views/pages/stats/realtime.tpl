
% rebase('base')

<div class="page-header">
    <h1 class="title">Statistics</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'stats') }}" class="tab-button">Overview</a>
        <span class="tab-button current">Realtime</span>
        <a href="{{ get_url(system, 'stats/history') }}" class="tab-button">History</a>
    </div>
</div>

% models = sorted({p.bus.model for p in positions if p.bus.model is not None})
% model_types = sorted({m.type for m in models})

<table class="striped">
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
            <tr class="section">
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
                    <td><a href="#{{ model.id }}">{{! model }}</a></td>
                    <td>{{ len([p for p in model_positions if p.trip is not None]) }}</td>
                    <td>{{ len([p for p in model_positions if p.trip is None]) }}</td>
                    <td>{{ len(model_positions) }}</td>
                </tr>
            % end
        % end
        <tr class="section">
            <td>Total</td>
            <td>{{ len([p for p in positions if p.trip is not None]) }}</td>
            <td>{{ len([p for p in positions if p.trip is None]) }}</td>
            <td>{{ len(positions) }}</td>
        </tr>
    </tbody>
</table>
