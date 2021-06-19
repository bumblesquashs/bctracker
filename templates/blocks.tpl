% rebase('base', title='Blocks')

<h1>Blocks</h1>
<hr />

% if system is None:
  <h2>Choose a System</h2>
  
  % include('components/systems')
% else:
  % blocks = system.all_blocks()
  % services = sorted({ b.service for b in blocks if b.service.is_current })

  <div class="list-container">
    <div class="list-navigation">
      % for service in services:
        <a href="#{{service}}" class='button'>{{ service }}</a>
      % end
    </div>
    <br />

    % for service in services:
      <div class="list-content">
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
                <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                <td>{{ block.routes_string }}</td>
                <td>{{ block.start_time }}</td>
              </tr>
            %end
          </tbody>
        </table>
      </div>
    % end
  </div>
% end
