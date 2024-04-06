
% rebase('base')

<div id="page-header">
    <h1>{{! model }}</h1>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Overview</h2>
            </div>
            <div class="content">
                <img class="photo" src="/img/models/vicinity.jpg">
                <p class="smaller-font lighter-text">Photo by Perrin Swanson</p>
                <div class="info-box">
                    <div class="row section">
                        <div class="name">Vehicle Type</div>
                        <div class="value">{{ model.type }}</div>
                    </div>
                    % if model.length is not None:
                        <div class="row section">
                            <div class="name">Length</div>
                            <div class="value">{{ model.length }} feet</div>
                        </div>
                    % end
                    % if model.fuel is not None:
                        <div class="row section">
                            <div class="name">Fuel Type</div>
                            <div class="value">{{ model.fuel }}</div>
                        </div>
                    % end
                </div>
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>Statistics</h2>
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="row section">
                        <div class="name">Total</div>
                        <div class="value">{{ sum([o.size for o in orders]) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Seen</div>
                        <div class="value">{{ len(overviews) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Tracked</div>
                        <div class="value">{{ len([o for o in overviews.values() if o.last_record]) }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container flex-3">
        <div class="section">
            <div class="header">
                <h2>Buses</h2>
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
                        % for order in orders:
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
    </div>
</div>
