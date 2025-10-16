
% rebase('base')

<div id="page-header">
    <h1>{{ context.vehicle_type }} History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'history') }}" class="tab-button">Last Seen</a>
        <span class="tab-button current">First Seen</span>
        <a href="{{ get_url(context, 'history', 'transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>

<div class="container">
    <div class="section">
        <div class="content">
            % if allocations:
                % if context.system:
                    <div class="options-container">
                        <div class="option" onclick="toggleShowTransfers()">
                            <div class="checkbox {{ 'selected' if show_transfers else '' }}">
                                % include('components/svg', name='status/check')
                            </div>
                            <div>Show Transfers</div>
                        </div>
                    </div>
                    <script>
                        function toggleShowTransfers() {
                            window.location = "{{! get_url(context, 'history', 'first-seen', show_transfers='false' if show_transfers else 'true') }}"
                        }
                    </script>
                % end
                % if any(a.first_record and a.first_record.warnings for a in allocations):
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
                                <th>Date</th>
                                <th>{{ context.vehicle_type }}</th>
                                <th class="desktop-only">Model</th>
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
                            % last_date = None
                            % for allocation in allocations:
                                % vehicle = allocation.vehicle
                                % record = allocation.first_record
                                % allocation_date = allocation.first_date
                                % if not last_date or allocation_date.year != last_date.year or allocation_date.month != last_date.month:
                                    <tr class="header">
                                        <td colspan="6">{{ allocation_date.format_month() }}</td>
                                        <tr class="display-none"></tr>
                                    </tr>
                                % end
                                % last_date = allocation_date
                                <tr>
                                    <td>
                                        <div class="column">
                                            {{ allocation_date.format_day() }}
                                            % if not context.system:
                                                <span class="mobile-only smaller-font">{{ allocation.context }}</span>
                                            % end
                                        </div>
                                    </td>
                                    <td>
                                        <div class="column">
                                            <div class="row space-between">
                                                % include('components/vehicle')
                                                % if context.system and not allocation.active:
                                                    <div class="transfer tooltip-anchor">
                                                        % include('components/svg', name='transfer')
                                                        <div class="tooltip right">Transferred</div>
                                                    </div>
                                                % end
                                            </div>
                                            <span class="non-desktop smaller-font">
                                                % include('components/year_model', year_model=vehicle.year_model)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/year_model', year_model=vehicle.year_model)
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
                        </tbody>
                    </table>
                </div>
            % else:
                <div class="placeholder">
                    % if not context.system:
                        <h3>No vehicle history found</h3>
                        <p>Something has probably gone terribly wrong if you're seeing this.</p>
                    % elif not context.realtime_enabled:
                        <h3>{{ context }} realtime information is not supported</h3>
                        <p>You can browse schedule data using the links above, or choose a different system.</p>
                        <div class="non-desktop">
                            % include('components/systems')
                        </div>
                    % else:
                        <h3>No {{ context }} {{ context.vehicle_type_plural.lower() }} have been recorded</h3>
                        <p>Please check again later!</p>
                    % end
                </div>
            % end
        </div>
    </div>
</div>

% include('components/top_button')
