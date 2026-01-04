
% rebase('base')

<div id="page-header">
    <h1>{{ context.vehicle_type }} History</h1>
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
                % if context.system:
                    <div class="options-container">
                        <div class="option" onclick="toggleShowTransfers()">
                            <div class="checkbox {{ 'selected' if show_transfers else '' }}">
                                % include('components/svg', name='status/check')
                            </div>
                            <div>Show Transfers</div>
                        </div>
                    </div>
                % end
                <script>
                    function setDays(days) {
                        if (days === null) {
                            window.location = "{{ get_url(context, 'history') }}";
                        } else {
                            window.location = "{{ get_url(context, 'history') }}?days=" + days;
                        }
                    }
                    
                    function toggleShowTransfers() {
                        window.location = "{{! get_url(context, 'history', days=days, show_transfers='false' if show_transfers else 'true') }}"
                    }
                </script>
            </div>
        </div>
        
        % if allocations:
            <div class="section closed">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Statistics</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % models = sorted({a.vehicle.model for a in allocations if a.vehicle.model})
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
                                % type_allocations = [a for a in allocations if a.vehicle.model and a.vehicle.model.type == model_type]
                                <tr class="header">
                                    <td>{{ model_type }}</td>
                                    <td class="align-right">{{ len(type_allocations) }}</td>
                                </tr>
                                <tr class="display-none"></tr>
                                % type_models = [m for m in models if m.type == model_type]
                                % for model in type_models:
                                    % model_allocations = [a for a in type_allocations if a.vehicle.model == model]
                                    <tr>
                                        <td>{{! model }}</td>
                                        <td class="align-right">{{ len(model_allocations) }}</td>
                                    </tr>
                                % end
                            % end
                            <tr class="header">
                                <td>Total</td>
                                <td class="align-right">{{ len(allocations) }}</td>
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
                <h2>{{ context.vehicle_type_plural }}</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if allocations:
                    % known_allocations = [a for a in allocations if a.vehicle.order_id]
                    % unknown_allocations = [a for a in allocations if not a.vehicle.order_id]
                    % if any(a.last_record and a.last_record.warnings for a in allocations):
                        <p>
                            <span>Entries with a</span>
                            <span class="record-warnings">
                                % include('components/svg', name='status/warning')
                            </span>
                            <span>may be accidental logins.</span>
                        </p>
                    % end
                    % if context.system and any(not a.active for a in allocations):
                        <p>
                            <span>Entries with a</span>
                            <span class="transfer">
                                % include('components/svg', name='transfer')
                            </span>
                            <span>have been transferred elsewhere.</span>
                        </p>
                    % end
                    <div class="table-border-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>{{ context.vehicle_type }}</th>
                                    <th>Last Seen</th>
                                    % if not context.system:
                                        <th class="non-mobile">System</th>
                                    % end
                                    % if context.enable_blocks:
                                        <th>Block</th>
                                        <th class="desktop-only">Routes</th>
                                    % else:
                                        <th>Routes</th>
                                    % end
                                </tr>
                            </thead>
                            <tbody>
                                % if unknown_allocations:
                                    <tr class="header">
                                        <td colspan="5">
                                            <div class="row space-between">
                                                <div>Unknown Year/Model</div>
                                                <div>{{ len(unknown_allocations) }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % for allocation in unknown_allocations:
                                        % vehicle = allocation.vehicle
                                        % record = allocation.last_record
                                        <tr>
                                            <td>
                                                <div class="row space-between">
                                                    % include('components/vehicle')
                                                    % if context.system and not allocation.active:
                                                        <div class="transfer tooltip-anchor">
                                                            % include('components/svg', name='transfer')
                                                            <div class="tooltip right">Transferred</div>
                                                        </div>
                                                    % end
                                                </div>
                                            </td>
                                            <td class="desktop-only">{{ allocation.last_date.format_long() }}</td>
                                            <td class="non-desktop">
                                                <div class="column">
                                                    {{ allocation.last_date.format_short() }}
                                                    % if not context.system:
                                                        <span class="mobile-only smaller-font">{{ allocation.context }}</span>
                                                    % end
                                                </div>
                                            </td>
                                            % if not context.system:
                                                <td class="non-mobile">{{ allocation.context }}</td>
                                            % end
                                            % if context.enable_blocks:
                                                % if record:
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
                                                % else:
                                                    <td colspan="2" class="lighter-text">No records for this system</td>
                                                % end
                                            % else:
                                                % if record:
                                                    <td>
                                                        % include('components/route_list', routes=record.routes)
                                                    </td>
                                                % else:
                                                    <td class="lighter-text">No records for this system</td>
                                                % end
                                            % end
                                        </tr>
                                    % end
                                % end
                                % for order in orders:
                                    % order_allocations = [a for a in known_allocations if a.vehicle.order_id == order.id]
                                    <tr class="header">
                                        <td colspan="5">
                                            <div class="row space-between">
                                                <div>{{! order }}</div>
                                                <div>{{ len(order_allocations) }} / {{ len(order.vehicles) }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % for allocation in order_allocations:
                                        % vehicle = allocation.vehicle
                                        % record = allocation.last_record
                                        <tr>
                                            <td>
                                                <div class="row space-between">
                                                    % include('components/vehicle')
                                                    % if context.system and not allocation.active:
                                                        <div class="transfer tooltip-anchor">
                                                            % include('components/svg', name='transfer')
                                                            <div class="tooltip right">Transferred</div>
                                                        </div>
                                                    % end
                                                </div>
                                            </td>
                                            <td class="desktop-only">{{ allocation.last_date.format_long() }}</td>
                                            <td class="non-desktop">
                                                <div class="column">
                                                    {{ allocation.last_date.format_short() }}
                                                    % if not context.system:
                                                        <span class="mobile-only smaller-font">{{ allocation.context }}</span>
                                                    % end
                                                </div>
                                            </td>
                                            % if not context.system:
                                                <td class="non-mobile">{{ allocation.context }}</td>
                                            % end
                                            % if context.enable_blocks:
                                                % if record:
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
                                                % else:
                                                    <td colspan="2" class="lighter-text">No records for this system</td>
                                                % end
                                            % else:
                                                % if record:
                                                    <td>
                                                        % include('components/route_list', routes=record.routes)
                                                    </td>
                                                % else:
                                                    <td class="lighter-text">No records for this system</td>
                                                % end
                                            % end
                                        </tr>
                                    % end
                                % end
                            </tbody>
                        </table>
                    </div>
        
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
                            <h3>No {{ context }} {{ context.vehicle_type_plural.lower() }} have been recorded for the selected date range</h3>
                            <p>Please choose a different date range or check again later!</p>
                        % else:
                            <h3>No {{ context }} {{ context.vehicle_type_plural.lower() }} have been recorded</h3>
                            <p>Please check again later!</p>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
</div>
