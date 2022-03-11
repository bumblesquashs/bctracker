% from models.system import get_system

% rebase('base', title='Routes')

<div class="page-header">
    <h1 class="title">Routes</h1>
</div>
<hr />

% if system is None:
    <p>
        Routes can only be viewed for individual systems.
        Please choose a system.
    </p>
    % include('components/systems')
% else:
    % routes = system.get_routes()
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
                        % include('components/services_indicator', services=route.services, compact=True)
                    </td>
                </tr>
            % end
        </tbody>
    </table>
% end
