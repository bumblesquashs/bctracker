
% rebase('base')

<div id="page-header">
    <h1>Fleet</h1>
</div>

% models = sorted({o.model for o in orders})
% model_types = sorted({m.type for m in models})

<div class="container">
    <div class="section">
        <div class="content">
            <p>
                This is the full list of vehicles that are currently available on BCTracker.
                It does not include every vehicle that has ever been operated in BC, but it should be mostly up-to-date with modern fleets.
                Many of the older units were retired long before BCTracker was started, but are included for the sake of completion.
            </p>
            <p>
                Any vehicle that is marked as <span class="lighter-text">Unavailable</span> has not been tracked.
                There are a few reasons why that may be the case:
            </p>
            <ol>
                <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                <li>It may not have been in service since BCTracker started tracking vehicles</li>
                <li>It may not have functional tracking equipment installed</li>
                <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
            </ol>
            <p>Vehicles that have been tracked before show the first and last date and system that they were seen in, even if they weren't in service.</p>
            % if context.system:
                <p>
                    Please note that this list includes vehicles from every system.
                    To see only {{ context }} {{ context.vehicle_type_plural.lower() }}, visit the <a href="{{ get_url(context, 'history') }}">history</a> page.
                </p>
            % end
        </div>
    </div>
    <div class="section">
        <div class="content">
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
                                        <th class="align-right">Seen</th>
                                        <th class="align-right">Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % buses = {a.bus for a in allocations}
                                    % for type in model_types:
                                        <tr class="header">
                                            <td>{{ type }}</td>
                                            <td class="align-right">{{ sum(1 for b in buses if b.model and b.model.type == type) }}</td>
                                            <td class="align-right">{{ sum(len(o.buses) for o in orders if o.model.type == type) }}</td>
                                        </tr>
                                        <tr class="display-none"></tr>
                                        % type_models = [m for m in models if m.type == type]
                                        % for model in type_models:
                                            <tr>
                                                <td><a href="#{{ model.id }}">{{! model }}</a></td>
                                                <td class="align-right">{{ sum(1 for b in buses if b.model and b.model == model) }}</td>
                                                <td class="align-right">{{ sum(len(o.buses) for o in orders if o.model == model) }}</td>
                                            </tr>
                                        % end
                                    % end
                                    <tr class="header">
                                        <td>Total</td>
                                        <td class="align-right">{{ sum(1 for b in buses if b.visible) }}</td>
                                        <td class="align-right">{{ sum(len(o.buses) for o in orders) }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="container flex-3">
                    % for type in model_types:
                        <div class="section">
                            <div class="header" onclick="toggleSection(this)">
                                <h2>{{ type }}</h2>
                                % include('components/toggle')
                            </div>
                            <div class="content">
                                <div class="container">
                                    % type_models = [m for m in models if m.type == type]
                                    % for model in type_models:
                                        % model_orders = [o for o in orders if o.model == model]
                                        <div id="{{ model.id }}" class="section">
                                            <div class="header" onclick="toggleSection(this)">
                                                <h3>{{! model }}</h3>
                                                % include('components/toggle')
                                            </div>
                                            <div class="content">
                                                <div class="table-border-wrapper">
                                                    <table>
                                                        <thead>
                                                            <tr>
                                                                <th>Vehicle</th>
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
                                                                            <div>{{ order.years_string }}</div>
                                                                            <div>{{ len(order.buses) }}</div>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                                <tr class="display-none"></tr>
                                                                % for bus in order.buses:
                                                                    % bus_allocations = [a for a in allocations if a.bus == bus]
                                                                    % if bus_allocations:
                                                                        % first_seen_date = min(a.first_seen for a in bus_allocations)
                                                                        % first_seen_context = min(bus_allocations).context
                                                                        % last_seen_date = max(a.last_seen for a in bus_allocations)
                                                                        % last_seen_context = max(bus_allocations).context
                                                                        <tr>
                                                                            <td>
                                                                                % include('components/bus')
                                                                            </td>
                                                                            <td class="desktop-only">{{ first_seen_date.format_long() }}</td>
                                                                            <td class="non-desktop">
                                                                                <div class="column">
                                                                                    {{ first_seen_date.format_short() }}
                                                                                    <span class="mobile-only smaller-font">{{ first_seen_context }}</span>
                                                                                </div>
                                                                            </td>
                                                                            <td class="non-mobile">{{ first_seen_context }}</td>
                                                                            <td class="desktop-only">{{ last_seen_date.format_long() }}</td>
                                                                            <td class="non-desktop">
                                                                                <div class="column">
                                                                                    {{ last_seen_date.format_short() }}
                                                                                    <span class="mobile-only smaller-font">{{ last_seen_context }}</span>
                                                                                </div>
                                                                            </td>
                                                                            <td class="non-mobile">{{ last_seen_context }}</td>
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
                                        </div>
                                    % end
                                </div>
                            </div>
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
</div>

% include('components/top_button')
