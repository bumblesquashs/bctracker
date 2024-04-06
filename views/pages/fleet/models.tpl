
% rebase('base')

<div id="page-header">
    <h1>Fleet</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'fleet') }}" class="tab-button">All Buses</a>
        <div class="tab-button current">By Model</div>
    </div>
</div>

% models = sorted({o.model for o in orders})
% model_types = sorted({m.type for m in models})

<div class="page-container">
    <div class="container flex-3">
        % for type in model_types:
            <div class="section">
                <div class="header">
                    <h2>{{ type }}</h2>
                </div>
                <div class="content">
                    <div class="grid-container">
                        % type_models = [m for m in models if m.type == type]
                        % for model in type_models:
                            <div class="section">
                                <div class="header">
                                    <h3>
                                        <a href="{{ get_url(system, f'fleet/models/{model.id}') }}">{{! model }}</a>
                                    </h3>
                                </div>
                                <div class="content">
                                    <img class="photo" src="/img/models/vicinity.jpg">
                                    <p class="smaller-font lighter-text">Photo by Perrin Swanson</p>
                                </div>
                            </div>
                        % end
                    </div>
                    <div class="container display-none">
                        % type_models = [m for m in models if m.type == type]
                        % for model in type_models:
                            % model_orders = [o for o in orders if o.model == model]
                            <div id="{{ model.id }}" class="section">
                                <div class="header">
                                    <h3>{{! model }}</h3>
                                </div>
                                <div class="content">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Bus</th>
                                                <th>First Seen</th>
                                                <th class="non-mobile">First System</th>
                                                <th>Last Seen</th>
                                                <th class="non-mobile">Last System</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % for order in model_orders:
                                                <tr class="header">
                                                    <td colspan="5">
                                                        <div class="row space-between">
                                                            <div>{{ order.year }}</div>
                                                            <div>{{ order.size }}</div>
                                                        </div>
                                                    </td>
                                                </tr>
                                                <tr class="display-none"></tr>
                                                % for bus in order:
                                                    % if bus.number in overviews:
                                                        % overview = overviews[bus.number]
                                                        <tr>
                                                            <td>
                                                                % include('components/bus')
                                                            </td>
                                                            <td class="desktop-only">{{ overview.first_seen_date.format_long() }}</td>
                                                            <td class="non-desktop">
                                                                <div class="column">
                                                                    {{ overview.first_seen_date.format_short() }}
                                                                    <span class="mobile-only smaller-font">{{ overview.first_seen_system }}</span>
                                                                </div>
                                                            </td>
                                                            <td class="non-mobile">{{ overview.first_seen_system }}</td>
                                                            <td class="desktop-only">{{ overview.last_seen_date.format_long() }}</td>
                                                            <td class="non-desktop">
                                                                <div class="column">
                                                                    {{ overview.last_seen_date.format_short() }}
                                                                    <span class="mobile-only smaller-font">{{ overview.last_seen_system }}</span>
                                                                </div>
                                                            </td>
                                                            <td class="non-mobile">{{ overview.last_seen_system }}</td>
                                                        </tr>
                                                    % else:
                                                        <tr>
                                                            <td>
                                                                % include('components/bus', enable_link=False)
                                                            </td>
                                                            <td class="lighter-text" colspan="4">Unavailable</td>
                                                        </tr>
                                                    % end
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
    </div>
</div>

% include('components/top_button')
