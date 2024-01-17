
% rebase('base')

<div class="page-header">
    <h1>Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'blocks/{block.id}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'blocks/{block.id}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
</div>

% if system.realtime_enabled:
    <div class="flex-container">
        % if len(records) > 0:
            <div class="sidebar container flex-1">
                <div class="section">
                    <div class="header">
                        <h2>Overview</h2>
                    </div>
                    <div class="content">
                        <div class="info-box">
                            <div class="section">
                                % include('components/events_indicator', events=events)
                            </div>
                            <div class="column section">
                                % orders = sorted({r.bus.order for r in records if r.bus.order is not None})
                                % for order in orders:
                                    % percentage = (len([r for r in records if r.bus.order == order]) / len(records)) * 100
                                    <div class="row">
                                        <div class="flex-1">{{! order }}</div>
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
                <div class="header">
                    <h2>History</h2>
                </div>
                <div class="content">
                    % if len(records) == 0:
                        <div class="placeholder">
                            <h3>This block doesn't have any recorded history</h3>
                            <p>There are a few reasons why that might be the case:</p>
                            <ol>
                                <li>It may be a new block introduced in the last service change</li>
                                <li>It may not be operating due to driver or vehicle shortages</li>
                                <li>It may have only been done by buses without functional NextRide equipment installed</li>
                            </ol>
                            <p>Please check again later!</p>
                        </div>
                    % else:
                        % if len([r for r in records if len(r.warnings) > 0]) > 0:
                            <p>
                                <span>Entries with a</span>
                                <img class="middle-align white inline" src="/img/white/warning.png" />
                                <img class="middle-align black inline" src="/img/black/warning.png" />
                                <span>may be accidental logins.</span>
                            </p>
                        % end
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Bus</th>
                                    <th class="desktop-only">Model</th>
                                    <th class="non-mobile">First Seen</th>
                                    <th>Last Seen</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for record in records:
                                    % bus = record.bus
                                    % order = bus.order
                                    <tr>
                                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                                        <td class="non-desktop">{{ record.date.format_short() }}</td>
                                        <td>
                                            <div class="column">
                                                <div class="row">
                                                    % include('components/bus', bus=bus)
                                                    % include('components/record_warnings_indicator', record=record)
                                                </div>
                                                <span class="non-desktop smaller-font">
                                                    % include('components/order', order=order)
                                                </span>
                                            </div>
                                        </td>
                                        <td class="desktop-only">
                                            % include('components/order', order=order)
                                        </td>
                                        <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                        <td>{{ record.last_seen.format_web(time_format) }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    % end
                </div>
            </div>
        </div>
    </div>
    
    % include('components/top_button')
% else:
    <div class="placeholder">
        <h3>{{ system }} does not currently support realtime</h3>
        <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
    </div>
% end
