<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th>Block</th>
      <th>Routes</th>
      <th class="desktop-only">Start Time</th>
      <th class="mobile-only">Start</th>
    </tr>
  </thead>

  <tbody>
    % for block in blocks:
      <tr>
        <td><a href="{{ get_url(block.system.id, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
        <td>{{ block.routes_string }}</td>
        <td>{{ block.start_time }}</td>
      </tr>
    %end
  </tbody>
</table>
  