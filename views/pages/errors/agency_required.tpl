
% rebase('base')

<div id="page-header">
    <h1>Select an Agency</h1>
</div>

<div class="placeholder">
    <h3>To see a bus you need to choose an agency</h3>
    <table>
        <thead>
            <tr>
                <th>Agency</th>
            </tr>
        </thead>
        <tbody>
            % for a in agencies:
                <tr>
                    <td>
                        <div class="row">
                            % include('components/agency_logo', agency=a)
                            <a href="{{ get_url(system, 'bus', a, bus_number) }}">{{ a }}</a>
                        </div>
                    </td>
                </tr>
            % end
        </tbody>
    </table>
</div>
