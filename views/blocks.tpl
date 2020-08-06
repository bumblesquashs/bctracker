% import datastructure as ds
% from formatting import format_time

% include('templates/header', title='All Blocks')

<h1>All Blocks</h1>
<hr />

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th>Block</th>
      <th>Routes</th>
      <th>Start Time</th>
      <th>Service Days</th>
    </tr>
  </thead>
  <tbody>
    % blocklist = list(ds.blockdict.values())
    % blocklist.sort(key = lambda x: (ds.service_order_dict.setdefault(x.serviceid, 10000), int(x.blockid)))
    % for block in blocklist:
      % b_routes = block.get_block_routes()
      % routes_entry = ''
      % for route in b_routes:
        % routes_entry += route + ', '
      % end
      % routes_entry = routes_entry[:-2] # drop the last comma and space
      <tr>
        <td><a href="blocks/{{block.blockid}}">{{ block.blockid }}</a></td>
        <td>{{ routes_entry }}</td>
        <td>{{ format_time(block.triplist[0].starttime) }}</td>
        <td>{{ ds.days_of_week_dict[block.serviceid] }}</td>
      </tr>
    % end
  </tbody>
</table>

% include('templates/footer')
