
% rebase('base')

<div id="page-header">
    <h1>Administration</h1>
    <h2>Tools for server and system management</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'admin') }}" class="tab-button">Management</a>
        <span class="tab-button current">Logs</span>
    </div>
</div>

<div class="container">
    <div class="section">
        <div class="content">
            % if len(logs) < 300:
                Showing {{ len(logs) }} lines
            % else:
                Showing last 300 of {{ len(logs) }} lines
            % end
            <div class="table-border-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th class="non-mobile">Timestamp</th>
                            <th class="non-mobile">Level</th>
                            <th>Message</th>
                        </tr>
                    </thead>
                    <tbody>
                        % logs.append('[2026-01-01 00:00:00] DEBUG: Testing debug UI')
                        % logs.append('[2026-01-01 00:00:00] INFO: Testing info UI')
                        % logs.append('[2026-01-01 00:00:00] WARNING: Testing warning UI')
                        % logs.append('[2026-01-01 00:00:00] ERROR: Testing error UI')
                        % logs.append('[2026-01-01 00:00:00] CRITICAL: Testing critical UI')
                        % for log in list(reversed(logs))[:300]:
                            % parts = log.split(': ', 1)
                            % data = parts[0]
                            % message = parts[1]
                            % data_parts = data.split('] ', 1)
                            % log_timestamp = data_parts[0][1:]
                            % level = data_parts[1]
                            <tr class="log-line {{ level.lower() }}">
                                <td>
                                    <div class="column">
                                        <div class="row title">
                                            % include('components/svg', name=f'status/{level.lower()}')
                                            {{ log_timestamp }}
                                        </div>
                                        <div class="mobile-only">{{ message }}</div>
                                    </div>
                                </td>
                                <td class="non-mobile level">{{ level.title() }}</td>
                                <td class="non-mobile">{{ message }}</td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
