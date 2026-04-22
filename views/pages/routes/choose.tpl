
% rebase('base')

<div id="page-header">
    <h1>Choose a Route</h1>
</div>

<p>
    Multiple routes found with the number {{ route_number }}.
    Please select which route you want to see.
</p>

% route_types = {r.type for r in routes}
<div class="container">
    % for route_type in route_types:
        % type_routes = [r for r in routes if r.type == route_type]
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>{{ route_type }} Services</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <table>
                    <thead>
                        <tr>
                            <th>Route</th>
                            <th>System</th>
                            <th class="non-mobile">Service Days</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for route in type_routes:
                            <tr>
                                <td>
                                    <div class="row">
                                        % include('components/route')
                                        <div class="column gap-5">
                                            <a href="{{ route.url() }}">{{! route.display_name }}</a>
                                            <div class="mobile-only">
                                                % include('components/weekdays', context=route.context, schedule=route.schedule, compact=True, schedule_path=f'routes/{route.url_id}/schedule')
                                            </div>
                                        </div>
                                    </div>
                                </td>
                                <td>{{ route.context }}</td>
                                <td class="non-mobile">
                                    % include('components/weekdays', context=route.context, schedule=route.schedule, compact=True, schedule_path=f'routes/{route.url_id}/schedule')
                                </td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        </div>
    % end
</div>
