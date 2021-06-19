
% rebase('base', title='Realtime')

<h1>Realtime</h1>
% if group == 'all':
  <h2>All active buses</h2>
% elif group == 'route':
  <h2>Routes with active buses</h2>
% elif group == 'model':
  <h2>Models with active buses</h2>
% end
<hr />

<div class="body list-container">
  % if len(buses) == 0:
    <div class="list-content">
      % if system is not None and not system.supports_realtime:
        {{ system }} does not currently support realtime.
        Please choose a different system.
      % else:
        There doesn't appear to be any buses out right now.
        BC Transit has no nightbus service, so this should be the case overnight.
        If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.
      % end
    </div>
  % else:
    <div class="list-navigation">
      % if group == 'all':
        <span class="button button-disabled">All Buses</span>
      % else:
        <a class="button" href="?group=all">All Buses</a>
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
      <span class="vertical-line desktop-only"></span>
      <div class="horizontal-line mobile-only"></div>
      % if group == 'all':
        <a class="button" href="?group=all&reload=true">Refresh Realtime</a>
      % elif group == 'route':
        <a class="button" href="?group=route&reload=true">Refresh Realtime</a>
      % elif group == 'model':
        <a class="button" href="?group=model&reload=true">Refresh Realtime</a>
      % end
    </div>
    <br />

    % if group == 'all':
      <div class="list-content">
        % include('components/realtime_list', buses=buses)
      </div>
    % elif group == 'route':
      % routes = sorted({b.position.trip.route for b in buses if b.position.trip is not None})
      
      % for route in routes:
        % route_buses = [b for b in buses if b.position.trip is not None and b.position.trip.route == route]
        <div class="list-content">
          <h2>{{ route }}</h2>
          % include('components/realtime_list', buses=route_buses)
        </div>
      % end
      
      % no_route_buses = [b for b in buses if b.position.trip is None]
      % if len(no_route_buses) > 0:
        <div class="list-content">
          <h2>Not In Service</h2>
          % include('components/realtime_list', buses=no_route_buses)
        </div>
      % end
    % elif group == 'model':
      % known_buses = [b for b in buses if b.range is not None]
      % models = sorted({b.range.model for b in known_buses})
      
      % for model in models:
        % model_buses = [b for b in known_buses if b.range.model == model]
        <div class="list-content">
          <h2>{{ model }}</h2>
          % include('components/realtime_list', buses=model_buses, show_model=False)
        </div>
      % end

      % unknown_buses = [b for b in buses if b.range is None]
      % if len(unknown_buses) > 0:
        <div class="list-content">
          <h2>Unknown Bus</h2>
          % include('components/realtime_list', buses=unknown_buses, show_model=False)
        </div>
      % end
    % end
  % end
</div>
