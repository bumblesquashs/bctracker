
% rebase('base', title='Realtime')

% import models.realtime as rt
% from models.realtime_position import RealtimeStatus
% realtime = rt.get_realtime()
% buses = realtime.get_realtime_positions(system)

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
    %    if system is None:
      <a class="button" href="{{ get_url(None, 'realtime') }}">All Buses</a>
    %    else:
      <a class="button" href="{{ get_url(system.id, 'realtime') }}">All Buses</a>
    %    end
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
    %    if system is None:
         <a class="button" href="{{ get_url(None, 'realtime') }}">All Buses</a>
    %    else:
         <a class="button" href="{{ get_url(system.id, 'realtime') }}">All Buses</a>
    %    end
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
<p>Last updated {{ realtime.pretty_last_updated_time }}</p>


% if not realtime.is_valid:
  <p>GTFS apparently out of date... need to fix that</p>
% end

% if len(buses) == 0:
  <p>There doesn't appear to be any buses out right now. BC Transit has no nightbus service, so this should be the case overnight. If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.</p>
% else:
  <%
    if group == 'all':
        include('components/realtime_list', buses=buses)
    elif group == 'route':
        buses_on_route = [b for b in buses if b.realtime_status == RealtimeStatus.ONROUTE]
        routes = {b.system.get_route(b.route_id) for b in buses_on_route}
        sorted_routes = sorted(routes, key=lambda r: int(r.number))
        for route in sorted_routes:
            selected_buses = [b for b in buses_on_route if b.system.get_route(b.route_id) == route]
            include('components/realtime_list', group_name='{0} {1}'.format(route.number, route.name), buses=selected_buses)
        end
        
        buses_off_route = [b for b in buses if b.realtime_status != RealtimeStatus.ONROUTE]
        if len(buses_off_route) > 0:
            include('components/realtime_list', group_name='Not In Service', buses=buses_off_route)
        end
    elif group == 'model':
        known_busses = [b for b in buses if b.bus is not None]
        unknown_busses = [b for b in buses if b.bus is None]
        models = {b.bus.model for b in known_busses}
        sorted_models = sorted(models)
        for model in sorted_models:
            selected_buses = [b for b in known_busses if b.bus.model == model]
            include('components/realtime_list', group_name=model, buses=selected_buses, show_model=False)
        end
        if len(unknown_busses) != 0:
            include('components/realtime_list', group_name="Unknown Bus", buses=unknown_busses, show_model=False)
        end
    end
  %>
% end
