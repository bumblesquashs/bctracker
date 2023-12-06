
% rebase('base')

<div class="page-header">
    <h1 class="title">Fleet</h1>
</div>

<p>
    This is the full list of vehicles that are currently available on BCTracker.
    It does not include every bus that has ever been operated by BC Transit, but it should be mostly up-to-date with orders since the 1990s.
    Many of the older units were retired long before BCTracker was started, but are included for the sake of completion.
</p>
<p>
    Any vehicle that is marked as <span class="lighter-text">Unavailable</span> has not been tracked.
    There are a few reasons why that may be the case:
</p>
<ol>
    <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
    <li>It may not have been in service since BCTracker started tracking buses</li>
    <li>It may not have functional NextRide equipment installed</li>
    <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
</ol>
<p>Vehicles that have been tracked before show the first and last date and system that they were seen in, even if they weren't in service.</p>
% if system is not None:
    <p>
        Please note that this list includes vehicles from every system.
        To see only buses that have operated in {{ system }}, visit the <a href="{{ get_url(system, 'history') }}">history</a> page.
    </p>
% end

% models = sorted({o.model for o in orders})
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
                            <th>Tracked</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for type in model_types:
                            <tr class="section">
                                <td>{{ type }}</td>
                                <td>{{ len([o for o in overviews.values() if o.bus.model is not None and o.bus.model.type == type]) }}</td>
                                <td>{{ sum([o.size for o in orders if o.model.type == type]) }}</td>
                            </tr>
                            <tr class="display-none"></tr>
                            % type_models = [m for m in models if m.type == type]
                            % for model in type_models:
                                <tr>
                                    <td><a href="#{{ model.id }}">{{! model }}</a></td>
                                    <td>{{ len([o for o in overviews.values() if o.bus.model is not None and o.bus.model == model]) }}</td>
                                    <td>{{ sum([o.size for o in orders if o.model == model]) }}</td>
                                </tr>
                            % end
                        % end
                        <tr class="section">
                            <td>Total</td>
                            <td>{{ len([o for o in overviews.values() if o.bus.visible]) }}</td>
                            <td>{{ sum([o.size for o in orders]) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div class="container flex-3">
        % for type in model_types:
            <div class="section">
                <div class="header">
                    <h2>{{ type }}</h2>
                </div>
                <div class="content">
                    <div class="container">
                        % type_models = [m for m in models if m.type == type]
                        % for model in type_models:
                            % model_orders = [o for o in orders if o.model == model]
                            <div id="{{ model.id }}" class="section">
                                <div class="header">
                                    <h3>{{! model }}</h3>
                                </div>
                                <div class="content">
                                    <table class="striped">
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
                                                <tr class="section">
                                                    <td colspan="5">
                                                        <div class="flex-row">
                                                            <div class="flex-1">{{ order.year }}</div>
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
                                                                % include('components/bus', bus=bus)
                                                            </td>
                                                            <td class="desktop-only">{{ overview.first_seen_date.format_long() }}</td>
                                                            <td class="non-desktop">
                                                                <div class="flex-column">
                                                                    {{ overview.first_seen_date.format_short() }}
                                                                    <span class="mobile-only smaller-font">{{ overview.first_seen_system }}</span>
                                                                </div>
                                                            </td>
                                                            <td class="non-mobile">{{ overview.first_seen_system }}</td>
                                                            <td class="desktop-only">{{ overview.last_seen_date.format_long() }}</td>
                                                            <td class="non-desktop">
                                                                <div class="flex-column">
                                                                    {{ overview.last_seen_date.format_short() }}
                                                                    <span class="mobile-only smaller-font">{{ overview.last_seen_system }}</span>
                                                                </div>
                                                            </td>
                                                            <td class="non-mobile">{{ overview.last_seen_system }}</td>
                                                        </tr>
                                                    % else:
                                                        <tr>
                                                            <td>
                                                                % include('components/bus', bus=bus, enable_link=False)
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
