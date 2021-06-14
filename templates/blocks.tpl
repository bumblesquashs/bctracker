% rebase('base', title='Blocks')

<h1>Blocks</h1>
<hr />

% blocks = system.all_blocks()
% services = sorted({ b.service for b in blocks if b.service.is_current })

<p>
  % for service in services:
    <a href="#{{service}}" class='button spaced-button'>{{ service }}</a>
  % end
</p>

<div class="floating-container">
  % for service in services:
    <div class="floating-content">
      <h2 id="{{service}}">{{ service }}</h2>
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
          % service_blocks = [block for block in blocks if block.service == service]
          % for block in service_blocks:
            <tr>
              <td><a href="{{ get_url(block.system.id, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
              <td>{{ block.routes_string }}</td>
              <td>{{ block.start_time }}</td>
            </tr>
          %end
        </tbody>
      </table>
    </div>
  % end
</div>
