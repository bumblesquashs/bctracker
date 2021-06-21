% from formatting import format_date, format_date_mobile

% rebase('base', title='History')

<h1>History</h1>
<hr />

<div class="body">
  % if system is not None and not system.supports_realtime:
    <p>
      {{ system }} does not currently support realtime. Please choose a different system.
    </p>

    % include('components/systems', realtime_only=True)
  % else:
    <table class="pure-table pure-table-horizontal pure-table-striped">
      <thead>
        <tr>
          <th class="desktop-only">Bus Number</th>
          <th class="desktop-only">Year and Model</th>
          <th class="mobile-only">Bus</th>
          <th>Last Seen</th>
          % if system is None:
            <th class="desktop-only">System</th>
          % end
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
            <td class="desktop-only">{{ format_date(history.date) }}</td>
            <td class="mobile-only">{{ format_date_mobile(history.date) }}</td>
            % if system is None:
              <td class="desktop-only">{{ history.system }}</td>
            % end
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
  % end
</div>