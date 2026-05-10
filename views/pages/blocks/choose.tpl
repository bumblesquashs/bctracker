
% rebase('base')

<div id="page-header">
    <h1>Choose a Block</h1>
</div>

<p>
    Multiple blocks found with the ID {{ block_id }}.
    Please select which block you want to see.
</p>

<table>
    <thead>
        <tr>
            <th>Block</th>
            <th class="non-mobile">System</th>
            <th>Routes</th>
            <th class="non-mobile">Start Time</th>
            <th class="non-mobile">End Time</th>
            <th class="mobile-only">Time</th>
            <th class="desktop-only">Duration</th>
        </tr>
    </thead>
    <tbody>
        % for block in blocks:
            % start_time = block.get_start_time().format_web(time_format)
            % end_time = block.get_end_time().format_web(time_format)
            <tr>
                <td><a href="{{ block.url() }}">{{ block.id }}</a></td>
                <td class="non-mobile">{{ block.context }}</td>
                <td>
                    <div class="column">
                        % include('components/route_list', routes=block.get_routes())
                        <div class="mobile-only smaller-font">{{ block.context }}</div>
                    </div>
                </td>
                <td class="non-mobile">{{ start_time }}</td>
                <td class="non-mobile">{{ end_time }}</td>
                <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                <td class="desktop-only">{{ block.get_duration() }}</td>
            </tr>
        % end
    </tbody>
</table>
