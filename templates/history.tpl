% from formatting import format_date, format_date_mobile

% rebase('base', title='History')

<h1>History</h1>
<hr />

<div class="body">
  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th class="desktop-only">Bus Number</th>
        <th class="desktop-only">Year and Model</th>
        <th class="mobile-only">Bus</th>
        <th>Last Seen</th>
        <th class="desktop-only">System</th>
        <th class="desktop-only">Assigned Block</th>
        <th class="desktop-only">Assigned Routes</th>
        <th class="mobile-only">Block</th>
      </tr>
    </thead>
    <tbody>
      % for history in last_seen:
        % bus = history.bus
        <tr>
          <td>
            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
            <span class="mobile-only smaller-font">
              <br />
              {{ bus.range }}
            </span>
          </td>
          <td class="desktop-only">{{ bus.range }}</td>
          <td>
            <span class="desktop-only">{{ format_date(history.date) }}</span>
            <span class="mobile-only">{{ format_date_mobile(history.date) }}</span>
          </td>
          <td class="desktop-only">{{ history.system }}</td>
          <td>
            % if history.is_current:
              % block = history.block
              <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
            % else:
              <span>{{ history.block_id }}</span>
            % end
          </td>
          <td class="desktop-only">{{ ', '.join([str(r) for r in history.routes]) }}</td>
        </tr>
      % end
    </tbody>
  </table>
</div>