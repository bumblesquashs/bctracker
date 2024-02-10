
% rebase('base')

<div class="page-header">
    <h1 class="title">Administration</h1>
    <h2 class="subtitle">Tools for server and system management</h2>
</div>

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Server Management</h2>
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
            <div class="header">
                <h2>System Management</h2>
            </div>
            <div class="content">
                <div class="container">
                    % if system is None:
                        % for region in regions:
                            % region_systems = [s for s in systems if s.region == region]
                            <div class="section">
                                <div class="header">
                                    <h3>{{ region }}</h3>
                                </div>
                                <div class="content">
                                    <div class="container inline">
                                        % for region_system in region_systems:
                                            <div class="section">
                                                <div class="header">
                                                    <h4>{{ region_system }}</h4>
                                                </div>
                                                <div class="content">
                                                    <div class="button-container">
                                                        % if region_system.gtfs_enabled:
                                                            <div class="button" onclick="reloadGTFS('{{ region_system.id }}')">Reload GTFS</div>
                                                        % end
                                                        % if region_system.realtime_enabled:
                                                            <div class="button" onclick="reloadRealtime('{{ region_system.id }}')">Reload Realtime</div>
                                                        % end
                                                    </div>
                                                </div>
                                            </div>
                                        % end
                                    </div>
                                </div>
                            </div>
                        % end
                    % else:
                        <div class="section">
                            <div class="header">
                                <h3>{{ system }}</h3>
                            </div>
                            <div class="content">
                                <div class="button-container">
                                    % if system.gtfs_enabled:
                                        <div class="button" onclick="reloadGTFS('{{ system.id }}')">Reload GTFS</div>
                                    % end
                                    % if system.realtime_enabled:
                                        <div class="button" onclick="reloadRealtime('{{ system.id }}')">Reload Realtime</div>
                                    % end
                                </div>
                            </div>
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    let systemID
    
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

% if system is None:
    <script>
        systemID = null;
    </script>
% else:
    <script>
        systemID = "{{ system.id }}"
    </script>
% end
