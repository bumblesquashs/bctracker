
% from repositories import SystemRepository

% system_repository = di[SystemRepository]

% rebase('base')

<div id="page-header">
    <h1>Administration</h1>
    <h2>Tools for server and system management</h2>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Server Management</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="button-container">
                    <div class="button" onclick="reloadAdornments()">Reload Adornments</div>
                    <div class="button" onclick="reloadOrders()">Reload Orders</div>
                    <div class="button" onclick="reloadSystems()">Reload Systems</div>
                    <div class="button" onclick="reloadThemes()">Reload Themes</div>
                    <div class="button" onclick="restartCron()">Restart Cron</div>
                    <div class="button" onclick="backupDatabase()">Backup Database</div>
                </div>
            </div>
        </div>
    </div>
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>System Management</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="container">
                    <table>
                        <thead>
                            <tr>
                                <th>System</th>
                                <th>Enabled</th>
                                <th>GTFS</th>
                                <th>Realtime</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for region in regions:
                                % region_systems = [s for s in system_repository.find_all(enabled_only=False) if s.region == region]
                                % if region_systems:
                                    <tr class="header">
                                        <td class="section" colspan="11">{{ region }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % for region_system in sorted(region_systems):
                                        <tr>
                                            <td>
                                                <div class="row">
                                                    % include('components/agency_logo', agency=region_system.agency)
                                                    {{ region_system }}
                                                </div>
                                            </td>
                                            <td class="{{ 'positive' if region_system.enabled else 'negative' }}">
                                                % if region_system.enabled:
                                                    % include('components/svg', name='check-circle')
                                                % else:
                                                    % include('components/svg', name='close-circle')
                                                % end
                                            </td>
                                            <td>
                                                % if region_system.gtfs_enabled:
                                                    <div class="row">
                                                        <div class="positive">
                                                            % include('components/svg', name='check-circle')
                                                        </div>
                                                        <div class="button icon" onclick="reloadGTFS('{{ region_system.id }}')">
                                                            % include('components/svg', name='refresh')
                                                        </div>
                                                    </div>
                                                % else:
                                                    <div class="negative">
                                                        % include('components/svg', name='close-circle')
                                                    </div>
                                                % end
                                            </td>
                                            <td>
                                                % if region_system.realtime_enabled:
                                                    <div class="row">
                                                        <div class="positive">
                                                            % include('components/svg', name='check-circle')
                                                        </div>
                                                        <div class="button icon" onclick="reloadRealtime('{{ region_system.id }}')">
                                                            % include('components/svg', name='refresh')
                                                        </div>
                                                    </div>
                                                % else:
                                                    <div class="negative">
                                                        % include('components/svg', name='close-circle')
                                                    </div>
                                                % end
                                            </td>
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
</div>

<script>
    function reloadAdornments() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/reload-adornments"), true);
        request.send();
    }
    
    function reloadOrders() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/reload-orders"), true);
        request.send();
    }
    
    function reloadSystems() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/reload-systems"), true);
        request.send();
    }
    
    function reloadThemes() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/reload-themes"), true);
        request.send();
    }
    
    function restartCron() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/restart-cron"), true);
        request.send();
    }
    
    function backupDatabase() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/backup-database"), true);
        request.send();
    }
    
    function reloadGTFS(reloadSystemID) {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/reload-gtfs/" + reloadSystemID), true);
        request.send();
    }
    
    function reloadRealtime(reloadSystemID) {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(systemID, "api/admin/reload-realtime/" + reloadSystemID), true);
        request.send();
    }
</script>
