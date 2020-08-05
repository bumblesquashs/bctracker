% import businfotable as businfo
% import realtime as rt

% include('templates/header', title='Realtime')

<h1>Realtime</h1>
<h2>All currently active buses</h2>
% if rt.data_valid:
  <p>Data current to: {{time_string}} Pacific Time</p>
% else:
  <p>GTFS Apparently out of date... need to fix that</p>
  <p>Data current to: {{time_string}} Pacific Time</p>
% end
<hr />

<p><a class="button" href="?rt=reload">Refresh Realtime</a></p>

% if len(rtbuslist) == 0:
  <p>There doesn't appear to be any buses out right now. Victoria has no nightbus service, so this should be the case overnight. If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.</p>
% else:
  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th>Fleet Number</th>
        <th>Year and Model</th>
        <th>Headsign</th>
        <th>Current Block</th>
        <th>Current Trip</th>
        <th>Current Stop</th>
      </tr>
    </thead>
    <tbody>
    % for bus in rtbuslist:
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
          <td>Unknown</td>
          <td>N/A</td>
        % else:
          <td><a href="/bus/number/{{bus.fleetnum}}">{{bus.fleetnum}}</a></td>
          %busrange = businfo.get_bus_range(bus.fleetnum)
          <td>{{busrange.year}} {{busrange.model}}</td>
        % end

        % if (bus.scheduled):
          <td>{{headsign}}</td>
          <td><a href="/blocks/{{blockid}}">{{blockid}}</a></td>
          <td><a href="/trips/{{tripid}}">{{tripid}}</a></td>
          % if bus.onroute:
            <td><a href="/stops/{{stopcode}}">{{stopcode}}</a></td>
          % else:
            <td>Not on route</td>
          % end
        % else:
          <td>Not in service</td>
          <td></td>
          <td></td>
          <td></td>
        %end
      </tr>
      %end
    </tbody>
  </table>
% end

% include('templates/footer')
