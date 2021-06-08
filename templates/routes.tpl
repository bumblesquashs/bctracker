% include('components/header', title='All Routes')

<h1>All Routes</h1>
<hr />

<table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
        <tr>
            <th>Route</th>
        </tr>
    </thead>
    <tbody>
        % for route in system.all_routes():
            <tr>
                <td><a href="routes/{{route.number}}">{{ route }}</a></td>
            </tr>
        % end
    </tbody>
</table>

% include('components/footer')
