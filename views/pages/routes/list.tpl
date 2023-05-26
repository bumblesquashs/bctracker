
% rebase('base')

<div class="page-header">
    <h1 class="title">Routes</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">List</span>
        <a href="{{ get_url(system, 'routes/map') }}" class="tab-button">Map</a>
    </div>
</div>

% if system is None:
    <p>Choose a system to see individual routes.</p>
    <table class="striped">
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
                    <tr class="section">
                        <td colspan="3">
                            {{ region }}
                        </td>
                    </tr>
                    <tr class="display-none"></tr>
                    % for region_system in region_systems:
                        % count = len(region_system.get_routes())
                        <tr>
                            <td>
                                <div class="flex-column">
                                    <a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
                                    <span class="mobile-only smaller-font">
                                        % if count == 1:
                                            1 Route
                                        % else:
                                            {{ count }} Routes
                                        % end
                                    </span>
                                </div>
                            </td>
                            <td class="non-mobile">{{ count }}</td>
                            <td>
                                % include('components/weekdays_indicator', schedule=region_system.schedule, compact=True)
                            </td>
                        </tr>
                    % end
                % end
            % end
        </tbody>
    </table>
% else:
    % routes = system.get_routes()
    % if len(routes) == 0:
        <p>
            Route information is currently unavailable for {{ system }}.
            Please check again later!
        </p>
        <div class="non-desktop">
            % include('components/systems')
        </div>
    % else:
        <table class="striped">
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
                            <div class="flex-row">
                                % include('components/route_indicator')
                                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                            </div>
                        </td>
                        <td class="non-mobile">
                            % include('components/weekdays_indicator', schedule=route.schedule, compact=True, url=get_url(system, f'routes/{route.number}/schedule'))
                        </td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end
