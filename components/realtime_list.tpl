
<table class="pure-table pure-table-horizontal pure-table-striped fixed-table">
  <thead>
    <tr>
      <th class="desktop-only">Number</th>
      % if get('show_model', True):
        <th class="desktop-only">Model</th>
        <th class="mobile-only">Bus</th>
      % else:
        <th class="desktop-only">Year</th>
        <th class="mobile-only" style="width: 20%;">Bus</th>
      % end
      % if system is None:
        <th class="desktop-only">System</th>
      % end
      <th>Headsign</th>
      <th class="desktop-only">Current Block</th>
      <th class="desktop-only">Current Trip</th>
      <th class="desktop-only">Current Stop</th>
    </tr>
  </thead>
  <tbody>
    % last_bus = None
    % for bus in sorted(buses):
      % position = bus.position
      % same_model = last_bus is None or bus.order == last_bus.order
      % last_bus = bus
      <tr class="{{'' if same_model else 'divider'}}">
        % if bus.number is None:
          <td>Unknown Bus</td>
          <td class="desktop-only"></td>
        % else:
          % order = bus.order
          <td>
            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus.number }}</a>
            % if order is not None:
              <span class="mobile-only smaller-font">
                <br />
                {{ order.year }}
                % if get('show_model', True):
                    {{ order.model }}
                % end
              </span>
            % end
          </td>
          <td class="desktop-only">
            % if order is not None:
              {{ order.year }}
              % if get('show_model', True):
                  {{ order.model }}
              % end
            % end
          </td>
        % end
        % if system is None:
          <td class="desktop-only">{{ position.system }}</td>
        % end
        % if position.trip is None:
          <td class="lighter-text">Not in service</td>
          <td class="desktop-only"></td>
          <td class="desktop-only"></td>
          <td class="desktop-only"></td>
        % else:
          % trip = position.trip
          % block = position.trip.block
          <td>{{ trip }}</td>
          <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
          <td class="desktop-only"><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
          % if position.stop is None:
            <td class="desktop-only lighter-text">Unavailable</td>
          % else:
            % stop = position.stop
            <td class="desktop-only"><a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a></td>
          % end
        %end
      </tr>
    %end
  </tbody>
</table>
