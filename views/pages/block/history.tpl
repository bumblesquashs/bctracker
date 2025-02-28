
% rebase('base')

<div id="page-header">
    <h1>Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'blocks', block) }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, 'blocks', block, 'map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
</div>

% if system.realtime_enabled:
    <div class="page-container">
        % if records:
            <div class="sidebar container flex-1">
                <div class="section">
                    <div class="header" onclick="toggleSection(this)">
                        <h2>Overview</h2>
                        % include('components/toggle')
                    </div>
                    <div class="content">
                        <div class="info-box">
                            <div class="section">
                                % include('components/events_list', events=events)
                            </div>
                            <div class="column section">
                                % orders = sorted({r.bus.order for r in records if r.bus.order})
                                % for order in orders:
                                    % percentage = (len([r for r in records if r.bus.order == order]) / len(records)) * 100
                                    <div class="row space-between">
                                        <div>{{! order }}</div>
                                        <div class="lighter-text">{{ round(percentage) }}%</div>
                                    </div>
                                % end
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        % end
        
        <div class="container flex-3">
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>History</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if records:
                        % if [r for r in records if r.warnings]:
                            <p>
                                <span>Entries with a</span>
                                <span class="record-warnings">
                                    % include('components/svg', name='warning')
                                </span>
                                <span>may be accidental logins.</span>
                            </p>
                        % end
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Bus</th>
                                    <th class="desktop-only">Model</th>
                                    <th class="no-wrap non-mobile">First Seen</th>
                                    <th class="no-wrap">Last Seen</th>
                                </tr>
                            </thead>
                            <tbody>
                                % last_date = None
                                % for record in records:
                                    % bus = record.bus
                                    % if not last_date or record.date.year != last_date.year or record.date.month != last_date.month:
                                        <tr class="header">
                                            <td colspan="5">{{ record.date.format_month() }}</td>
                                            <tr class="display-none"></tr>
                                        </tr>
                                    % end
                                    % last_date = record.date
                                    <tr>
                                        <td>{{ record.date.format_day() }}</td>
                                        <td>
                                            <div class="column">
                                                <div class="row">
                                                    % include('components/bus')
                                                    % include('components/record_warnings')
                                                </div>
                                                <span class="non-desktop smaller-font">
                                                    % include('components/order', order=bus.order)
                                                </span>
                                            </div>
                                        </td>
                                        <td class="desktop-only">
                                            % include('components/order', order=bus.order)
                                        </td>
                                        <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                        <td>{{ record.last_seen.format_web(time_format) }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    % else:
                        <div class="placeholder">
                            <h3>This block doesn't have any recorded history</h3>
                            <p>There are a few reasons why that might be the case:</p>
                            <ol>
                                <li>It may be a new block introduced in the last service change</li>
                                <li>It may not be operating due to driver or vehicle shortages</li>
                                <li>It may have only been done by buses without functional tracking equipment installed</li>
                            </ol>
                            <p>Please check again later!</p>
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
    
    % include('components/top_button')
% else:
    <div class="placeholder">
        <h3>{{ system }} realtime information is not supported</h3>
        <p>You can browse schedule data using the links above, or choose a different system.</p>
    </div>
% end
