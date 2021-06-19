
<table class="pure-table pure-table-horizontal pure-table-striped fixed-table">
  <thead>
    <tr>
      % if system is None:
        <th class="desktop-only">System</th>
      % end
        <th class="desktop-only">Number</th>
      % if get('show_model', True):
        <th class="desktop-only">Year and Model</th>
        <th class="mobile-only">Bus</th>
      % else:
        <th class="desktop-only">Year</th>
        <th class="mobile-only" style="width: 20%;">Bus</th>
      % end
      <th>Headsign</th>
      <th class="desktop-only">Current Block</th>
      <th class="desktop-only">Current Trip</th>
      <th class="desktop-only">Current Stop</th>
    </tr>
  </thead>
  <tbody>
    % for bus in sorted(buses):
      % position = bus.position
      <tr>
        % if system is None:
          <td class="desktop-only">{{ position.system }}</td>
        % end
        % if bus.number is None:
          <td>Unknown Bus</td>
          <td class="desktop-only"></td>
        % else:
          % range = bus.range
          <td>
            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus.number }}</a>
            <span class="mobile-only smaller-font">
              <br />
              {{ range.year }}
              % if get('show_model', True):
                  {{ range.model }}
              % end
            </span>
          </td>
          <td class="desktop-only">
            {{ range.year }}
            % if get('show_model', True):
                {{ range.model }}
            % end
          </td>
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
