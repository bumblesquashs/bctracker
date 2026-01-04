
% from models.log import LogLevel

% rebase('base')

<div id="page-header">
    <h1>Administration</h1>
    <h2>Tools for server and system management</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'admin') }}" class="tab-button">Management</a>
        <span class="tab-button current">Logs</span>
    </div>
</div>

<div class="page-container">
    <div class="container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Filter by Level</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="section">
                        <div class="options-container grid">
                            <div class="option" onclick="setLevel(null)">
                                <div class="radio-button {{ 'selected' if level is None else '' }}"></div>
                                <div>All Logs</div>
                            </div>
                            <div class="option" onclick="setLevel('debug')">
                                <div class="radio-button {{ 'selected' if level == LogLevel.DEBUG else '' }}"></div>
                                <div>Debug</div>
                            </div>
                            <div class="option" onclick="setLevel('info')">
                                <div class="radio-button {{ 'selected' if level == LogLevel.INFO else '' }}"></div>
                                <div>Info</div>
                            </div>
                            <div class="option" onclick="setLevel('warning')">
                                <div class="radio-button {{ 'selected' if level == LogLevel.WARNING else '' }}"></div>
                                <div>Warning</div>
                            </div>
                            <div class="option" onclick="setLevel('error')">
                                <div class="radio-button {{ 'selected' if level == LogLevel.ERROR else '' }}"></div>
                                <div>Error</div>
                            </div>
                            <div class="option" onclick="setLevel('critical')">
                                <div class="radio-button {{ 'selected' if level == LogLevel.CRITICAL else '' }}"></div>
                                <div>Critical</div>
                            </div>
                        </div>
                    </div>
                </div>
                <script>
                    function setLevel(level) {
                        if (level === null) {
                            window.location = "{{ get_url(context, 'admin', 'logs') }}";
                        } else {
                            window.location = "{{ get_url(context, 'admin', 'logs') }}?level=" + level;
                        }
                    }
                </script>
            </div>
        </div>
    </div>
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Logs</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if len(logs) == total_logs:
                    Showing {{ len(logs) }} lines
                % else:
                    Showing {{ len(logs) }} of {{ total_logs }} lines
                % end
                % if logs:
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
                                % for log in logs:
                                    <tr class="log-line {{ log.level.value }}">
                                        <td>
                                            <div class="column">
                                                <div class="row title">
                                                    % include('components/svg', name=f'status/{log.level.value}')
                                                    {{ log.timestamp }}
                                                </div>
                                                <div class="mobile-only">{{ log.message }}</div>
                                            </div>
                                        </td>
                                        <td class="non-mobile level">{{ log.level }}</td>
                                        <td class="non-mobile">{{ log.message }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    </div>
                % end
            </div>
        </div>
    </div>
</div>