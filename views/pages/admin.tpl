
% rebase('base', title='Administration')

<div class="page-header">
    <h1 class="title">Administration</h1>
    <h2 class="subtitle">Tools for server and system management</h2>
    <hr />
</div>

<div class="container no-inline">
    <div class="section">
        <h2 class="title">Server Management</h2>
        <div class="button-container">
            <div class="button" onclick="restartCron()">Restart Cron</div>
            <div class="button" onclick="backupDatabase()">Backup Database</div>
        </div>
    </div>
    <div class="section">
        <h2 class="title">System Management</h2>
        <div class="container no-inline">
            % if system is None:
                % for admin_system in admin_systems:
                    <div class="section">
                        <h3 class="title">{{ admin_system }}</h3>
                        <div class="subtitle">
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
                % end
            % else:
                <div class="section">
                    <h3 class="title">{{ system }}</h3>
                    <div class="subtitle">
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
                    </div>
                    <div class="button-container">
                        % if system.gtfs_enabled:
                            <div class="button">Reload GTFS</div>
                        % end
                        % if system.realtime_enabled:
                            <div class="button">Reload Realtime</div>
                        % end
                    </div>
                </div>
            % end
        </div>
    </div>
</div>

<script>
    let adminKey
    let systemID
    
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