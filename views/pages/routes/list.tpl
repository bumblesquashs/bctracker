
% rebase('base', title='Routes')

<div class="page-header">
    <h1 class="title">Routes</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">List</span>
        <a href="{{ get_url(system, 'routes/map') }}" class="tab-button">Map</a>
    </div>
    <hr />
</div>

% if system is None:
    <p>
        Routes can only be viewed for individual systems.
        Please choose a system.
    </p>
    % include('components/systems')
% else:
    % routes = system.get_routes()
    % if len(routes) == 0:
        <p>
            Route information is currently unavailable for {{ system }}.
            Please check again later!
        </p>
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
                            % include('components/service_pattern_indicator', pattern=route.service_group, compact=True)
                        </td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
% end
