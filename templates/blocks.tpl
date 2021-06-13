% rebase('base', title='All Blocks')

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
    % for block in sorted(system.all_blocks()):
      <tr>
        <td>
          <a href="{{ get_url(block.system.id, f'/blocks/{block.id}') }}">
            {{ block.id }}
          </a>
          <span class="mobile-only smaller-font">
            <br />
            {{ block.routes_string }}
          </span>
        </td>
        <td class="desktop-only">{{ block.routes_string }}</td>
        <td>{{ block.start_time }}</td>
        <td class="no-wrap">{{ block.service }}</td>
      </tr>
    % end
  </tbody>
</table>
