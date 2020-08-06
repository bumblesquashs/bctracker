% include('templates/header', title='Route {0}'.format(routenum))

<h1>{{routenum}} {{routename}}</h1>
All trips for Route {{routenum}} by the time of their first stop
<hr />

<div class="desktop-only side-menu">
  <div class="side-menu-header">
    <b>Navigation</b>
  </div>
  <div class="side-menu-content">
    % for day_str in day_order:
      % trip_list = day_triplistdict[day_str]
      % ib_trips = [trip for trip in trip_list if trip.directionid == '0']
      % ob_trips = [trip for trip in trip_list if trip.directionid == '1']
      <p>
        <b>{{day_str}}</b>
        % if (len(ob_trips) != 0):
          <br />
          <a href="#{{day_str}}_ob">Outbound Trips</a>
        % end

        % if (len(ib_trips) != 0):
          <br />
          <a href="#{{day_str}}_ib">Inbound Trips</a>
        % end
      </p>
    %end
  </div>
</div>

<div class="body">
  % for day_str in day_order:
    % trip_list = day_triplistdict[day_str]
    % ib_trips = [trip for trip in trip_list if trip.directionid == '0']
    % ob_trips = [trip for trip in trip_list if trip.directionid == '1']
    <h2 id="{{day_str}}">{{day_str}}</h2>
  
    % if(len(ob_trips) != 0):
      <h3 id="{{day_str}}_ob">Outbound</h3>
      <p class="subtitle">{{len(ob_trips)}} Trips</p>
      
      % include('templates/triplist', triplist=ob_trips)
    % end
  
    % if(len(ib_trips) != 0):
      <h3 id="{{day_str}}_ib">Inbound</h3>
      <p class="subtitle">{{len(ib_trips)}} Trips</p>
      
      % include('templates/triplist', triplist=ib_trips)
    % end
  %end
</div>

% include('templates/footer')
