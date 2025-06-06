
% rebase('base')

<div id="page-header">
    <h1>Routes</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">List</span>
        <a href="{{ get_url(context, 'routes', 'map') }}" class="tab-button">Map</a>
    </div>
</div>

% if context.system:
    % routes = context.system.get_routes()
    % if routes:
        <table>
            <thead>
                <tr>
                    <th>Route</th>
                    <th class="non-mobile">Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for route in routes:
                    <tr>
                        <td>
                            <div class="row">
                                % include('components/route')
                                <a href="{{ get_url(route.context, 'routes', route) }}">{{! route.display_name }}</a>
                            </div>
                        </td>
                        <td class="non-mobile">
                            % include('components/weekdays', schedule=route.schedule, compact=True, schedule_path=f'routes/{route.url_id}/schedule')
                        </td>
                    </tr>
                % end
            </tbody>
        </table>
    % else:
        <div class="placeholder">
            <h3>{{ context }} route information is unavailable</h3>
            % if context.gtfs_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        </div>
    % end
% else:
    <div class="placeholder">
        <p>Choose a system to see individual routes.</p>
        <table>
            <thead>
                <tr>
                    <th>System</th>
                    <th class="non-mobile align-right">Routes</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if region_systems:
                        <tr class="header">
                            <td colspan="3">{{ region }}</td>
                        </tr>
                        <tr class="display-none"></tr>
                        % for system in sorted(region_systems):
                            % count = len(system.get_routes())
                            <tr>
                                <td>
                                    <div class="row">
                                        % include('components/agency_logo', agency=system.agency)
                                        <div class="column">
                                            <a href="{{ get_url(system.context, *path) }}">{{ system }}</a>
                                            <span class="mobile-only smaller-font">
                                                % if system.gtfs_loaded:
                                                    % if count == 1:
                                                        1 Route
                                                    % else:
                                                        {{ count }} Routes
                                                    % end
                                                % end
                                            </span>
                                        </div>
                                    </div>
                                </td>
                                % if system.gtfs_loaded:
                                    <td class="non-mobile align-right">{{ count }}</td>
                                    <td>
                                        % include('components/weekdays', schedule=system.schedule, compact=True)
                                    </td>
                                % else:
                                    <td class="lighter-text" colspan="2">Routes are loading...</td>
                                % end
                            </tr>
                        % end
                    % end
                % end
            </tbody>
        </table>
    </div>
% end
