% include('templates/header', title='All Routes')

<h1>All Routes</h1>
<hr />

<table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
        <tr>
            <th>Route</th>
        </tr>
    </thead>
    <tbody>
        % for routeid in rdict:
            <tr>
                <td><a href="routes/{{rdict[routeid][0]}}">{{rdict[routeid][0]}} {{rdict[routeid][1]}}</a></td>
            </tr>
        % end
    </tbody>
</table>

% include('templates/footer')
