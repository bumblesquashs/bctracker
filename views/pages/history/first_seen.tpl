
% rebase('base')

<div id="page-header">
    <h1>Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'history') }}" class="tab-button">Last Seen</a>
        <span class="tab-button current">First Seen</span>
        <a href="{{ get_url(context, 'history', 'transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>

<div class="container">
    <div class="section">
        <div class="content">
            % if overviews:
                % if [o for o in overviews if o.first_record and o.first_record.warnings]:
                    <p>
                        <span>Entries with a</span>
                        <span class="record-warnings">
                            % include('components/svg', name='status/warning')
                        </span>
                        <span>may be accidental logins.</span>
                    </p>
                % end
                <div class="table-border-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Bus</th>
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
                            % for overview in overviews:
                                % record = overview.first_record
                                % bus = record.bus
                                % if not last_date or record.date.year != last_date.year or record.date.month != last_date.month:
                                    <tr class="header">
                                        <td colspan="6">{{ record.date.format_month() }}</td>
                                        <tr class="display-none"></tr>
                                    </tr>
                                % end
                                % last_date = record.date
                                <tr>
                                    <td>
                                        <div class="column">
                                            {{ record.date.format_day() }}
                                            % if not context.system:
                                                <span class="mobile-only smaller-font">{{ record.context }}</span>
                                            % end
                                        </div>
                                    </td>
                                    <td>
                                        <div class="column">
                                            % include('components/bus')
                                            <span class="non-desktop smaller-font">
                                                % include('components/year_model', year_model=bus.year_model)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/year_model', year_model=bus.year_model)
                                    </td>
                                    % if not context.system:
                                        <td class="non-mobile">{{ record.context }}</td>
                                    % end
                                    % if context.enable_blocks:
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
                                        <td>
                                            % include('components/route_list', routes=record.routes)
                                        </td>
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
                        <h3>No {{ context }} buses have been recorded</h3>
                        <p>Please check again later!</p>
                    % end
                </div>
            % end
        </div>
    </div>
</div>

% include('components/top_button')
