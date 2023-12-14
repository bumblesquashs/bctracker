
% rebase('base')

<div class="page-header">
    <h1 class="title">Administration</h1>
    <h2 class="subtitle">Tools for server and system management</h2>
</div>

<div class="container">
    <div class="section">
        <div class="header">
            <h2>Server Management</h2>
        </div>
        <div class="content">
            <div class="button-container">
                <div class="button" onclick="reloadIcons()">Reload Icons</div>
                <div class="button" onclick="reloadOrders()">Reload Orders</div>
                <div class="button" onclick="reloadSystems()">Reload Systems</div>
                <div class="button" onclick="reloadThemes()">Reload Themes</div>
                <div class="button" onclick="restartCron()">Restart Cron</div>
                <div class="button" onclick="backupDatabase()">Backup Database</div>
            </div>
        </div>
    </div>
    <div class="section">
        <div class="header">
            <h2>System Management</h2>
        </div>
        <div class="content">
            <div class="container">
                % if system is None:
                    % for admin_system in admin_systems:
                        <div class="section">
                            <div class="header">
                                <h3>{{ admin_system }}</h3>
                            </div>
                            <div class="content">
                                <div>
                                    Enabled:
                                    % if admin_system.enabled:
                                        <span class="positive">Yes</span>
                                    % else:
                                        <span class="negative">No</span>
                                    % end
                                </div>
                                <div>
                                    Visible:
                                    % if admin_system.visible:
                                        <span class="positive">Yes</span>
                                    % else:
                                        <span class="negative">No</span>
                                    % end
                                </div>
                                <div class="button-container">
                                    % if admin_system.gtfs_enabled:
                                        <div class="button" onclick="reloadGTFS('{{ admin_system.id }}')">Reload GTFS</div>
                                    % end
                                    % if admin_system.realtime_enabled:
                                        <div class="button" onclick="reloadRealtime('{{ admin_system.id }}')">Reload Realtime</div>
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
                            <div>
                                Enabled:
                                % if system.enabled:
                                    <span class="positive">Yes</span>
                                % else:
                                    <span class="negative">No</span>
                                % end
                            </div>
                            <div>
                                Visible:
                                % if system.visible:
                                    <span class="positive">Yes</span>
                                % else:
                                    <span class="negative">No</span>
                                % end
                            </div>
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

<script>
    let adminKey
    let systemID
    
    function reloadIcons() {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/reload-icons"), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/reload-icons"), true);
        }
        request.send();
    }
    
    function reloadOrders() {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/reload-orders"), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/reload-orders"), true);
        }
        request.send();
    }
    
    function reloadSystems() {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/reload-systems"), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/reload-systems"), true);
        }
        request.send();
    }
    
    function reloadThemes() {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/reload-themes"), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/reload-themes"), true);
        }
        request.send();
    }
    
    function restartCron() {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/restart-cron"), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/restart-cron"), true);
        }
        request.send();
    }
    
    function backupDatabase() {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/backup-database"), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/backup-database"), true);
        }
        request.send();
    }
    
    function reloadGTFS(reloadSystemID) {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/reload-gtfs/" + reloadSystemID), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/reload-gtfs/" + reloadSystemID), true);
        }
        request.send();
    }
    
    function reloadRealtime(reloadSystemID) {
        const request = new XMLHttpRequest();
        if (adminKey == null) {
            request.open("POST", getUrl(systemID, "api/admin/reload-realtime/" + reloadSystemID), true);
        } else {
            request.open("POST", getUrl(systemID, "api/admin/" + adminKey + "/reload-realtime/" + reloadSystemID), true);
        }
        request.send();
    }
</script>

% if key is None:
    <script>
        adminKey = null;
    </script>
% else:
    <script>
        adminKey = "{{ key }}";
    </script>
% end

% if system is None:
    <script>
        systemID = null;
    </script>
% else:
    <script>
        systemID = "{{ system.id }}"
    </script>
% end
