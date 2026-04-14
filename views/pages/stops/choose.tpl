
% rebase('base')

<div id="page-header">
    <h1>Choose a Stop</h1>
</div>

<p>
    Multiple stops found with the code {{ stop_number }}.
    Please select which stop you want to see.
</p>

<table>
    <thead>
        <tr>
            <th>Stop</th>
            <th class="non-mobile">System</th>
            <th class="non-mobile">Routes</th>
            <th>Service Days</th>
        </tr>
    </thead>
    <tbody>
        % for stop in stops:
            <tr>
                <td>
                    <div class="column">
                        % include('components/stop')
                        <div class="mobile-only smaller-font">{{ stop.context }}</div>
                        <div class="mobile-only">
                            % include('components/route_list', routes=stop.routes)
                        </div>
                    </div>
                </td>
                <td class="non-mobile">{{ stop.context }}</td>
                <td class="non-mobile">
                    % include('components/route_list', routes=stop.routes)
                </td>
                <td>
                    % include('components/weekdays', schedule=stop.schedule, compact=True, schedule_path=f'stops/{stop.url_id}/schedule')
                </td>
            </tr>
        % end
    </tbody>
</table>
