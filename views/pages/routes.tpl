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
    % routes = system.get_routes(sheet)
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
                        % include('components/services_indicator', services=route.get_services(sheet), compact=True)
                    </td>
                </tr>
            % end
        </tbody>
    </table>
    
    % if system.id == 'chilliwack' or system.id == 'cfv':
        % fvx = get_system('fvx')
        <table class="striped">
            <thead>
                <tr>
                    <th>Fraser Valley Express (FVX)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><a href="{{ get_url(fvx, 'routes/66') }}">66 Fraser Valley Express</a></td>
                </tr>
            </tbody>
        </table>
    % end
    
    % if system.id == 'fvx':
        % cfv = get_system('cfv')
        % chilliwack = get_system('chilliwack')
        <table class="striped">
            <thead>
                <tr>
                    <th>Related Systems</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><a href="{{ get_url(cfv, 'routes') }}">Central Fraser Valley</a></td>
                </tr>
                <tr>
                    <td><a href="{{ get_url(chilliwack, 'routes') }}">Chilliwack</a></td>
                </tr>
            </tbody>
        </table>
    % end
% end
