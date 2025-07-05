
% rebase('base')

<div id="page-header">
    <h1>Vehicle History</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Last Seen</span>
        <a href="{{ get_url(context, 'history', 'first-seen') }}" class="tab-button">First Seen</a>
        <a href="{{ get_url(context, 'history', 'transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section {{ '' if days else 'closed' }}">
            <div class="header" onclick="toggleSection(this)">
                <h2>Filter by Date</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="section">
                        <div class="options-container grid">
                            <div class="option" onclick="setDays(1)">
                                <div class="radio-button {{ 'selected' if days == 1 else '' }}"></div>
                                <div>Today</div>
                            </div>
                            <div class="option" onclick="setDays(7)">
                                <div class="radio-button {{ 'selected' if days == 7 else '' }}"></div>
                                <div>Last Week</div>
                            </div>
                            <div class="option" onclick="setDays(31)">
                                <div class="radio-button {{ 'selected' if days == 31 else '' }}"></div>
                                <div>Last Month</div>
                            </div>
                            <div class="option" onclick="setDays(90)">
                                <div class="radio-button {{ 'selected' if days == 90 else '' }}"></div>
                                <div>Last 3 Months</div>
                            </div>
                            <div class="option" onclick="setDays(365)">
                                <div class="radio-button {{ 'selected' if days == 365 else '' }}"></div>
                                <div>Last Year</div>
                            </div>
                            <div class="option" onclick="setDays(null)">
                                <div class="radio-button {{ 'selected' if days is None else '' }}"></div>
                                <div>All Time</div>
                            </div>
                        </div>
                    </div>
                </div>
                <script>
                    function setDays(days) {
                        if (days === null) {
                            window.location = "{{ get_url(context, 'history') }}";
                        } else {
                            window.location = "{{ get_url(context, 'history') }}?days=" + days;
                        }
                    }
                </script>
            </div>
        </div>
        
        % if overviews:
            <div class="section closed">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Statistics</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % models = sorted({o.bus.model for o in overviews if o.bus.model})
                    % model_types = sorted({m.type for m in models})
                    <table>
                        <thead>
                            <tr>
                                <th>Model</th>
                                <th class="align-right">Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for model_type in model_types:
                                % type_overviews = [o for o in overviews if o.bus.model and o.bus.model.type == model_type]
                                <tr class="header">
                                    <td>{{ model_type }}</td>
                                    <td class="align-right">{{ len(type_overviews) }}</td>
                                </tr>
                                <tr class="display-none"></tr>
                                % type_models = [m for m in models if m.type == model_type]
                                % for model in type_models:
                                    % model_overviews = [o for o in type_overviews if o.bus.model == model]
                                    <tr>
                                        <td>{{! model }}</td>
                                        <td class="align-right">{{ len(model_overviews) }}</td>
                                    </tr>
                                % end
                            % end
                            <tr class="header">
                                <td>Total</td>
                                <td class="align-right">{{ len(overviews) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        % end
    </div>
    
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Vehicles</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if overviews:
                    % known_overviews = [o for o in overviews if o.bus.order]
                    % unknown_overviews = [o for o in overviews if not o.bus.order]
                    % orders = sorted({o.bus.order for o in known_overviews})
                    % if [o for o in overviews if o.last_record and o.last_record.warnings]:
                        <p>
                            <span>Entries with a</span>
                            <span class="record-warnings">
                                % include('components/svg', name='status/warning')
                            </span>
                            <span>may be accidental logins.</span>
                        </p>
                    % end
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th>Last Seen</th>
                                % if not context.system:
                                    <th class="non-mobile">System</th>
                                % end
                                <th>Block</th>
                                <th class="desktop-only">Routes</th>
                            </tr>
                        </thead>
                        <tbody>
                            % if unknown_overviews:
                                <tr class="header">
                                    <td colspan="5">
                                        <div class="row space-between">
                                            <div>Unknown Year/Model</div>
                                            <div>{{ len(unknown_overviews) }}</div>
                                        </div>
                                    </td>
                                </tr>
                                <tr class="display-none"></tr>
                                % for overview in unknown_overviews:
                                    % record = overview.last_record
                                    % bus = overview.bus
                                    <tr>
                                        <td>
                                            % include('components/bus')
                                        </td>
                                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                                        <td class="non-desktop">
                                            <div class="column">
                                                {{ record.date.format_short() }}
                                                % if not context.system:
                                                    <span class="mobile-only smaller-font">{{ record.context }}</span>
                                                % end
                                            </div>
                                        </td>
                                        % if not context.system:
                                            <td class="non-mobile">{{ record.context }}</td>
                                        % end
                                        <td>
                                            <div class="column">
                                                <div class="row space-between">
                                                    % if record.is_available:
                                                        % block = record.block
                                                        <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                                    % else:
                                                        <span>{{ record.block_id }}</span>
                                                    % end
                                                    % include('components/record_warnings')
                                                </div>
                                                <div class="non-desktop">
                                                    % include('components/route_list', routes=record.routes)
                                                </div>
                                            </div>
                                        </td>
                                        <td class="desktop-only">
                                            % include('components/route_list', routes=record.routes)
                                        </td>
                                    </tr>
                                % end
                            % end
                            % for order in orders:
                                % order_overviews = [o for o in known_overviews if o.bus.order == order]
                                <tr class="header">
                                    <td colspan="5">
                                        <div class="row space-between">
                                            <div>{{! order }}</div>
                                            <div>{{ len(order_overviews) }}</div>
                                        </div>
                                    </td>
                                </tr>
                                <tr class="display-none"></tr>
                                % for overview in order_overviews:
                                    % record = overview.last_record
                                    % bus = overview.bus
                                    <tr>
                                        <td>
                                            % include('components/bus')
                                        </td>
                                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                                        <td class="non-desktop">
                                            <div class="column">
                                                {{ record.date.format_short() }}
                                                % if not context.system:
                                                    <span class="mobile-only smaller-font">{{ record.context }}</span>
                                                % end
                                            </div>
                                        </td>
                                        % if not context.system:
                                            <td class="non-mobile">{{ record.context }}</td>
                                        % end
                                        <td>
                                            <div class="column stretch">
                                                <div class="row space-between">
                                                    % if record.is_available:
                                                        % block = record.block
                                                        <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                                    % else:
                                                        <span>{{ record.block_id }}</span>
                                                    % end
                                                    % include('components/record_warnings')
                                                </div>
                                                <div class="non-desktop">
                                                    % include('components/route_list', routes=record.routes)
                                                </div>
                                            </div>
                                        </td>
                                        <td class="desktop-only">
                                            % include('components/route_list', routes=record.routes)
                                        </td>
                                    </tr>
                                % end
                            % end
                        </tbody>
                    </table>
        
                    % include('components/top_button')
                % else:
                    <div class="placeholder">
                        % if not context.system:
                            % if days:
                                <h3>No vehicle history found for selected date range</h3>
                                <p>Please choose a different date range or check again later!</p>
                            % else:
                                <h3>No vehicle history found</h3>
                                <p>Something has probably gone terribly wrong if you're seeing this.</p>
                            % end
                        % elif not context.realtime_enabled:
                            <h3>{{ context }} realtime information is not supported</h3>
                            <p>You can browse schedule data using the links above, or choose a different system.</p>
                            <div class="non-desktop">
                                % include('components/systems')
                            </div>
                        % elif days:
                            <h3>No {{ context }} buses have been recorded for the selected date range</h3>
                            <p>Please choose a different date range or check again later!</p>
                        % else:
                            <h3>No {{ context }} buses have been recorded</h3>
                            <p>Please check again later!</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>
