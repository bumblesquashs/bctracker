
% rebase('base', title='Routes')

<div class="page-header">
    <h1 class="title">Routes</h1>
    % if system is not None:
        <div class="tab-button-bar">
            <span class="tab-button current">List</span>
            <a href="{{ get_url(system, 'routes/map') }}" class="tab-button">Map</a>
        </div>
    % end
    <hr />
</div>

% if system is None:
    <p>Choose a system to see individual routes.</p>
    <table class="striped">
        <thead>
            <tr>
                <th>System</th>
                <th># Routes</th>
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
                        <tr>
                            <td><a href="{{ get_url(region_system, path) }}">{{ region_system }}</a></td>
                            <td>{{ len(region_system.get_routes()) }}</td>
                            <td>
                                % include('components/schedule_indicator', schedule=region_system.schedule, compact=True)
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
                    <th>Service Days</th>
                </tr>
            </thead>
            <tbody>
                % for route in routes:
                    <tr>
                        <td><a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a></td>
                        <td>
                            % include('components/schedule_indicator', schedule=route.schedule, compact=True, url=get_url(system, f'routes/{route.number}/schedule'))
                        </td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end
