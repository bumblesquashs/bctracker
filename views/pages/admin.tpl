
% import repositories

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
                    <div class="button" onclick="reloadDecorations()">Reload Decorations</div>
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
                                <th class="non-mobile">Enabled</th>
                                <th class="non-mobile">Cache</th>
                                <th>GTFS</th>
                                <th>Realtime</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for region in regions:
                                % region_systems = [s for s in repositories.system.find_all(enabled_only=False) if s.region == region]
                                % if region_systems:
                                    <tr class="header">
                                        <td class="section" colspan="11">{{ region }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % for system in sorted(region_systems):
                                        % total = len(system.routes) + len(system.stops) + len(system.trips)
                                        % progress = len(system.route_caches) + len(system.stop_caches) + len(system.trip_caches)
                                        <tr>
                                            <td>
                                                <div class="row">
                                                    % include('components/agency_logo', agency=system.agency)
                                                    <div class="column">
                                                        {{ system }}
                                                        <div class="mobile-only smaller-font {{ 'positive' if system.enabled else 'negative' }}">
                                                            {{ 'Enabled' if system.enabled else 'Disabled' }}
                                                        </div>
                                                        <div class="mobile-only smaller-font">
                                                            % include('components/percentage', numerator=progress, denominator=total, low_cutoff=60, high_cutoff=90, inverted=True)
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td class="non-mobile {{ 'positive' if system.enabled else 'negative' }}">
                                                % if system.enabled:
                                                    % include('components/svg', name='status/enabled')
                                                % else:
                                                    % include('components/svg', name='status/disabled')
                                                % end
                                            </td>
                                            <td class="non-mobile">
                                                % include('components/percentage', numerator=progress, denominator=total, low_cutoff=60, high_cutoff=90, inverted=True)
                                            </td>
                                            <td>
                                                % if system.gtfs_enabled:
                                                    <div class="row">
                                                        <div class="positive">
                                                            % include('components/svg', name='status/enabled')
                                                        </div>
                                                        <div class="button icon" onclick="reloadGTFS('{{ system.id }}')">
                                                            % include('components/svg', name='action/refresh')
                                                        </div>
                                                    </div>
                                                % else:
                                                    <div class="negative">
                                                        % include('components/svg', name='status/disabled')
                                                    </div>
                                                % end
                                            </td>
                                            <td>
                                                % if system.realtime_enabled:
                                                    <div class="row">
                                                        <div class="positive">
                                                            % include('components/svg', name='status/enabled')
                                                        </div>
                                                        <div class="button icon" onclick="reloadRealtime('{{ system.id }}')">
                                                            % include('components/svg', name='action/refresh')
                                                        </div>
                                                    </div>
                                                % else:
                                                    <div class="negative">
                                                        % include('components/svg', name='status/disabled')
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
    function reloadDecorations() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/reload-decorations"), true);
        request.send();
    }
    
    function reloadOrders() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/reload-orders"), true);
        request.send();
    }
    
    function reloadSystems() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/reload-systems"), true);
        request.send();
    }
    
    function reloadThemes() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/reload-themes"), true);
        request.send();
    }
    
    function restartCron() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/restart-cron"), true);
        request.send();
    }
    
    function backupDatabase() {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/backup-database"), true);
        request.send();
    }
    
    function reloadGTFS(reloadSystemID) {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/reload-gtfs/" + reloadSystemID), true);
        request.send();
    }
    
    function reloadRealtime(reloadSystemID) {
        const request = new XMLHttpRequest();
        request.open("POST", getUrl(currentSystemID, "api/admin/reload-realtime/" + reloadSystemID), true);
        request.send();
    }
</script>
