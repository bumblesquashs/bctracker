
% rebase('base')

<div id="page-header">
    <h1>Vehicle History</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Last Seen</span>
        <a href="{{ get_url(system, 'history/first-seen') }}" class="tab-button">First Seen</a>
        <a href="{{ get_url(system, 'history/transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Filter by Date</h2>
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="grid section">
                        <div class="radio-button-container" onclick="setDays(1)">
                            <div class="radio-button {{ 'selected' if days == 1 else '' }}"></div>
                            <div class="label">Today</div>
                        </div>
                        <div class="radio-button-container" onclick="setDays(7)">
                            <div class="radio-button {{ 'selected' if days == 7 else '' }}"></div>
                            <div class="label">Last Week</div>
                        </div>
                        <div class="radio-button-container" onclick="setDays(31)">
                            <div class="radio-button {{ 'selected' if days == 31 else '' }}"></div>
                            <div class="label">Last Month</div>
                        </div>
                        <div class="radio-button-container" onclick="setDays(90)">
                            <div class="radio-button {{ 'selected' if days == 90 else '' }}"></div>
                            <div class="label">Last 3 Months</div>
                        </div>
                        <div class="radio-button-container" onclick="setDays(365)">
                            <div class="radio-button {{ 'selected' if days == 365 else '' }}"></div>
                            <div class="label">Last Year</div>
                        </div>
                        <div class="radio-button-container" onclick="setDays(null)">
                            <div class="radio-button {{ 'selected' if days is None else '' }}"></div>
                            <div class="label">All Time</div>
                        </div>
                    </div>
                </div>
                <script>
                    function setDays(days) {
                        if (days === null) {
                            window.location = "{{ get_url(system, 'history') }}";
                        } else {
                            window.location = "{{ get_url(system, 'history') }}?days=" + days;
                        }
                    }
                </script>
            </div>
        </div>
        
        % if overviews:
            <div class="section">
                <div class="header">
                    <h2>Statistics</h2>
                </div>
                <div class="content">
                    % models = sorted({o.bus.model for o in overviews if o.bus.model is not None})
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
                                % type_overviews = [o for o in overviews if o.bus.model is not None and o.bus.model.type == model_type]
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
            <div class="header">
                <h2>Vehicles</h2>
            </div>
            <div class="content">
                % if len(overviews) == 0:
                    <div class="placeholder">
                        % if system is None:
                            % if days:
                                <h3>No vehicle history found for selected date range</h3>
                                <p>Please choose a different date range or check again later!</p>
                            % else:
                                <h3>No vehicle history found</h3>
                                <p>Something has probably gone terribly wrong if you're seeing this.</p>
                            % end
                        % elif not system.realtime_enabled:
                            <h3>{{ system }} does not currently support realtime</h3>
                            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
                            <div class="non-desktop">
                                % include('components/systems')
                            </div>
                        % elif days:
                            <h3>No buses have been recorded in {{ system }} for the selected date range</h3>
                            <p>Please choose a different date range or check again later!</p>
                        % else:
                            <h3>No buses have been recorded in {{ system }}</h3>
                            <p>Please check again later!</p>
                        % end
                    </div>
                % else:
                    % known_overviews = [o for o in overviews if o.bus.order is not None]
                    % unknown_overviews = [o for o in overviews if o.bus.order is None]
                    % orders = sorted({o.bus.order for o in known_overviews})
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th>Last Seen</th>
                                % if system is None:
                                    <th class="non-mobile">System</th>
                                % end
                                % if af_2024:
                                    <th>Trip</th>
                                % else:
                                    <th>Block</th>
                                % end
                                <th class="desktop-only">Routes</th>
                            </tr>
                        </thead>
                        <tbody>
                            % if len(unknown_overviews) > 0:
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
                                                % if system is None:
                                                    <span class="mobile-only smaller-font">{{ record.system }}</span>
                                                % end
                                            </div>
                                        </td>
                                        % if system is None:
                                            <td class="non-mobile">{{ record.system }}</td>
                                        % end
                                        <td>
                                            <div class="column">
                                                % if record.is_available:
                                                    % block = record.block
                                                    % if af_2024:
                                                        <a href="{{ get_url(block.system, f'trips/{block.id}') }}">{{ block }}</a>
                                                    % else:
                                                        % include('components/block')
                                                    % end
                                                % else:
                                                    <span>{{ record.block_id }}</span>
                                                % end
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
                                                % if system is None:
                                                    <span class="mobile-only smaller-font">{{ record.system }}</span>
                                                % end
                                            </div>
                                        </td>
                                        % if system is None:
                                            <td class="non-mobile">{{ record.system }}</td>
                                        % end
                                        <td>
                                            <div class="column">
                                                % if record.is_available:
                                                    % block = record.block
                                                    % if af_2024:
                                                        <a href="{{ get_url(block.system, f'trips/{block.id}') }}">{{ block }}</a>
                                                    % else:
                                                        % include('components/block')
                                                    % end
                                                % else:
                                                    <span>{{ record.block_id }}</span>
                                                % end
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
                % end
            </div>
        </div>
    </div>
</div>
