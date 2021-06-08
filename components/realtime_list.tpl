% if defined('group_name'):
  <h2>{{ group_name }}</h2>
% end

<table class="pure-table pure-table-horizontal pure-table-striped fixed-table">
  <thead>
    <tr>
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
        busid = bus.fleetid
        if (bus.scheduled):
          tripid = bus.tripid
          trip = tripdict[tripid]
          blockid = trip.blockid
          headsign = trip.headsign
        end
        
        if(bus.onroute):
          try:
            stopcode = stopdict[bus.stopid].stopcode
          except KeyError:
            rt.handle_key_error()
          end
        else:
          stopcode = ''
        end
      %>
      <tr>
        % if (bus.unknown_fleetnum_flag):
          <td>Unknown Bus</td>
          <td class="desktop-only"></td>
        % else:
          % busrange = businfo.get_bus_range(bus.fleetnum)
          <td>
            <a href="/bus/{{bus.fleetnum}}">{{ bus.fleetnum }}</a>
            <span class="mobile-only smaller-font">
              <br />
              {{ busrange.year }}
              % if get('show_model', True):
                {{ busrange.model }}
              % end
            </span>
          </td>
          <td class="desktop-only">
            {{ busrange.year }}
            % if get('show_model', True):
              {{ busrange.model }}
            % end
          </td>
        % end

        % if (bus.scheduled):
          <td>{{headsign}}</td>
          <td class="desktop-only"><a href="/blocks/{{blockid}}">{{ blockid }}</a></td>
          <td class="desktop-only"><a href="/trips/{{tripid}}">{{ tripid }}</a></td>
          % if bus.onroute:
            <td class="desktop-only"><a href="/stops/{{stopcode}}">{{ ds.stopdict[bus.stopid].stopname }}</a></td>
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
