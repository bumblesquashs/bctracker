
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
                    % if system:
                        <div class="section">
                            <div class="header" onclick="toggleSection(this)">
                                <h3>{{ system }}</h3>
                                % include('components/toggle')
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
                    % else:
                        % for region in regions:
                            % region_systems = [s for s in systems if s.region == region]
                            <div class="section">
                                <div class="header" onclick="toggleSection(this)">
                                    <h3>{{ region }}</h3>
                                    % include('components/toggle')
                                </div>
                                <div class="content">
                                    <div class="container inline">
                                        % for region_system in sorted(region_systems):
                                            <div class="section">
                                                <div class="header" onclick="toggleSection(this)">
                                                    <h4>{{ region_system }}</h4>
                                                    % include('components/toggle')
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
                    % end
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
