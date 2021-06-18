% from models.realtime_position import RealtimeStatus

% if defined('group_name'):
  <h2>{{ group_name }}</h2>
% end

<table class="pure-table pure-table-horizontal pure-table-striped fixed-table">
  <thead>
    <tr>
        <th class="desktop-only">System</th>
        <th class="desktop-only">Fleet Number</th>
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
    % for bus in buses:
      <%
        fleet_number = bus.fleet_number
        system = bus.system
        status = bus.realtime_status
        if status != RealtimeStatus.UNASSIGNED:
            trip_id = bus.trip_id
            block_id = bus.block_id
            status = bus.realtime_status
            trip = system.get_trip(trip_id)
            headsign = trip.headsign
        end
        
        if status == RealtimeStatus.ONROUTE:
          try:
              stop_code = system.get_stop(bus.stop_id).number
              stop_name = system.get_stop(bus.stop_id).name
          except KeyError:
              stop_code = ''
              stop_name = ''
          end
        else:
            stop_code = ''
            stop_name = ''
        end
      %>
      <tr>
          <td>{{ system.name }}</td>
        % if fleet_number is None:
          <td>Unknown Bus</td>
          <td class="desktop-only"></td>
        % else:
          % bus_range = bus.bus
          <td>
            <a href="{{ get_url(system.id, f'bus/{fleet_number}') }}">{{ fleet_number }}</a>
            <span class="mobile-only smaller-font">
              <br />
              {{ bus_range.year }}
              % if get('show_model', True):
                  {{ bus_range.model }}
              % end
            </span>
          </td>
          <td class="desktop-only">
            {{ bus_range.year }}
            % if get('show_model', True):
                {{ bus_range.model }}
            % end
          </td>
        % end

        % if status != RealtimeStatus.UNASSIGNED:
          <td>{{headsign}}</td>
          
          <td class="desktop-only"><a href="{{ get_url(system.id, f'blocks/{block_id}') }}">{{ block_id }}</a></td>
          <td class="desktop-only"><a href="{{ get_url(system.id, f'trips/{trip_id}') }}">{{ trip_id }}</a></td>
          % if status == RealtimeStatus.ONROUTE:
            <td class="desktop-only"><a href="{{ get_url(system.id, f'stops/{system.get_stop(bus.stop_id).number}') }}">{{ stop_name }}</a></td>
          % else:
            <td class="desktop-only lighter-text">Unavailable</td>
          % end
        % else:
          <td class="lighter-text">Not in service</td>
          <td class="desktop-only"></td>
          <td class="desktop-only"></td>
          <td class="desktop-only"></td>
        %end
      </tr>
    %end
  </tbody>
</table>
