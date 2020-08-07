% import datastructure as ds
% from formatting import format_time

% include('templates/header', title='All Blocks')

<h1>All Blocks</h1>
<hr />

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th class="desktop-only">Block</th>
      <th class="desktop-only">Routes</th>
      <th class="desktop-only">Start Time</th>
      <th class="desktop-only">Service Days</th>

      <th class="mobile-only">Block and Routes</th>
      <th class="mobile-only">Start</th>
      <th class="mobile-only">Days</th>
    </tr>
  </thead>
  <tbody>
    % blocklist = list(ds.blockdict.values())
    % blocklist.sort(key = lambda x: (ds.service_order_dict.setdefault(x.serviceid, 10000), int(x.blockid)))
    % for block in blocklist:
      % b_routes = block.get_block_routes()
      <tr>
        <td>
          <a href="blocks/{{block.blockid}}">{{ block.blockid }}</a>
          <span class="mobile-only smaller-font">
            <br />
            {{ ', '.join(sorted(b_routes)) }}
          </span>
        </td>
        <td class="desktop-only">{{ ', '.join(sorted(b_routes)) }}</td>
        <td>{{ format_time(block.triplist[0].starttime) }}</td>
        <td class="no-wrap">{{ ds.days_of_week_dict[block.serviceid] }}</td>
      </tr>
    % end
  </tbody>
</table>

% include('templates/footer')
