% import businfotable as businfo
% import realtime as rt
% import datastructure as ds

% include('templates/header', title='Realtime')

<h1>Realtime</h1>
<h2>All currently active buses</h2>
<hr />

<p><a class="button" href="?rt=reload">Refresh Realtime</a></p>
<p>Last updated {{time_string}}</p>

% if not rt.data_valid:
  <p>GTFS Apparently out of date... need to fix that</p>
% end

% if len(rtbuslist) == 0:
  <p>There doesn't appear to be any buses out right now. Victoria has no nightbus service, so this should be the case overnight. If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.</p>
% else:
  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th class="desktop-only">Fleet Number</th>
        <th class="desktop-only">Year and Model</th>
        <th class="mobile-only">Bus</th>
        <th>Headsign</th>
        <th class="desktop-only">Current Block</th>
        <th class="desktop-only">Current Trip</th>
        <th class="desktop-only">Current Stop</th>
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
            <td>Unknown Bus</td>
            <td class="desktop-only"></td>
          % else:
            % busrange = businfo.get_bus_range(bus.fleetnum)
            <td>
              <a href="/bus/{{bus.fleetnum}}">{{ bus.fleetnum }}</a>
              <span class="mobile-only smaller-font">
                <br />
                {{ busrange.year }} {{ busrange.model }}
              </span>
            </td>
            <td class="desktop-only">{{ busrange.year }} {{ busrange.model }}</td>
          % end

          % if (bus.scheduled):
            <td>{{headsign}}</td>
            <td class="desktop-only"><a href="/blocks/{{blockid}}">{{ blockid }}</a></td>
            <td class="desktop-only"><a href="/trips/{{tripid}}">{{ tripid }}</a></td>
            % if bus.onroute:
              <td class="desktop-only"><a href="/stops/{{stopcode}}">{{ ds.stopdict[bus.stopid].stopname }}</a></td>
            % else:
              <td class="desktop-only">Not on route</td>
            % end
          % else:
            <td>Not in service</td>
            <td class="desktop-only"></td>
            <td class="desktop-only"></td>
            <td class="desktop-only"></td>
          %end
        </tr>
      %end
    </tbody>
  </table>
% end

% include('templates/footer')
