
% rebase('base')

<div id="page-header">
    <h1>Routes</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">List</span>
        <a href="{{ get_url(system, 'routes/map') }}" class="tab-button">Map</a>
    </div>
</div>

% if system is None:
    <div class="placeholder">
        <p>Choose a system to see individual routes.</p>
        <table>
            <thead>
                <tr>
                    <th>System</th>
                    <th class="non-mobile"># Routes</th>
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if len(region_systems) > 0:
                        <tr class="header">
                            <td colspan="3">{{ region }}</td>
                        </tr>
                        <tr class="display-none"></tr>
                        % for region_system in region_systems:
                            % count = len(region_system.get_routes())
                            <tr>
                                <td>
                                    <div class="column">
                                        <a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
                                        <span class="mobile-only smaller-font">
                                            % if region_system.is_loaded:
                                                % if count == 1:
                                                    1 Route
                                                % else:
                                                    {{ count }} Routes
                                                % end
                                            % end
                                        </span>
                                    </div>
                                </td>
                                % if region_system.is_loaded:
                                    <td class="non-mobile">{{ count }}</td>
                                    <td>
                                        % include('components/weekdays', schedule=region_system.schedule, compact=True)
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
% else:
    % routes = system.get_routes()
    % if len(routes) == 0:
        <div class="placeholder">
            <h3>Route information for {{ system }} is unavailable</h3>
            % if system.is_loaded:
                <p>Please check again later!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        </div>
    % else:
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
                                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                            </div>
                        </td>
                        <td class="non-mobile">
                            % include('components/weekdays', schedule=route.schedule, compact=True, schedule_path=f'routes/{route.number}/schedule')
                        </td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end
