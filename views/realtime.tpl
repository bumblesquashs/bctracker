% import businfotable as businfo
% import realtime as rt
% import datastructure as ds

% include('templates/header', title='Realtime')

<h1>Realtime</h1>
% if group == 'all':
  <h2>All active buses</h2>
% elif group == 'route':
  <h2>Routes with active buses</h2>
% elif group == 'model':
  <h2>Models with active buses</h2>
% end
<hr />

<div class="mobile-only">
  <div class="flexbox-space-between">
    % if group == 'all':
      <span class="button button-disabled">All Buses</span>
    % else:
      <a class="button" href="/realtime">All Buses</a>
    % end

    % if group == 'route':
      <span class="button button-disabled">By Route</span>
    % else:
      <a class="button" href="?group=route">By Route</a>
    % end

    % if group == 'model':
      <span class="button button-disabled">By Model</span>
    % else:
      <a class="button" href="?group=model">By Model</a>
    % end
  </div>
  <div class="horizontal-line"></div>
</div>
<p>
  <span class="desktop-only">
    % if group == 'all':
      <span class="button button-disabled">All Buses</span>
    % else:
      <a class="button" href="/realtime">All Buses</a>
    % end

    % if group == 'route':
      <span class="button button-disabled">By Route</span>
    % else:
      <a class="button" href="?group=route">By Route</a>
    % end

    % if group == 'model':
      <span class="button button-disabled">By Model</span>
    % else:
      <a class="button" href="?group=model">By Model</a>
    % end
    <span class="vertical-line"></span>
  </span>
  <span>
    % if group == 'all':
    <a class="button" href="?rt=reload">Refresh Realtime</a>
    % elif group == 'route':
    <a class="button" href="?group=route&rt=reload">Refresh Realtime</a>
    % elif group == 'model':
    <a class="button" href="?group=model&rt=reload">Refresh Realtime</a>
    % end
  </span>
</p>
<p>Last updated {{time_string}}</p>

% if not rt.data_valid:
  <p>GTFS apparently out of date... need to fix that</p>
% end

% if len(rtbuslist) == 0:
  <p>There doesn't appear to be any buses out right now. Victoria has no nightbus service, so this should be the case overnight. If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.</p>
% else:
  <%
    if group == 'all':
      include('templates/realtime_list', buses=rtbuslist)
    elif group == 'route':
      buses_on_route = list(filter(lambda b: b.scheduled, rtbuslist))
      routes = set(map(lambda b: rdict[tripdict[b.tripid].routeid], buses_on_route))
      sorted_routes = sorted(routes, key=lambda r: int(r[0]))
      for route in sorted_routes:
        buses = list(filter(lambda b: tripdict[b.tripid].routeid == route[2], buses_on_route))
        include('templates/realtime_list', group_name='{0} {1}'.format(route[0], route[1]), buses=buses)
      end

      buses_off_route = list(filter(lambda b: not b.scheduled, rtbuslist))
      if len(buses_off_route) > 0:
        include('templates/realtime_list', group_name='Not in service', buses=buses_off_route)
      end
    elif group == 'model':
      models = set(map(lambda b: businfo.get_bus_range(b.fleetnum).model, rtbuslist))
      sorted_models = sorted(models)
      for model in sorted_models:
        buses = list(filter(lambda b: businfo.get_bus_range(b.fleetnum).model == model, rtbuslist))
        include('templates/realtime_list', group_name=model, buses=buses)
      end
    end
  %>
% end

% include('templates/footer')
