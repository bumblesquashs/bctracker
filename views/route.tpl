% include('templates/header', title='{0} {1}'.format(routenum, routename))

<h1>{{routenum}} {{routename}}</h1>
<hr />

<p>
  % for day_str in day_order:
    <a href="#{{day_str}}" class='button spaced-button'>{{ day_str }}</a>
  % end
</p>

% for day_str in day_order:
  % trip_list = day_triplistdict[day_str]
  % ib_trips = [trip for trip in trip_list if trip.directionid == '0']
  % ob_trips = [trip for trip in trip_list if trip.directionid == '1']
  <h2 id="{{day_str}}">{{day_str}}</h2>

  % if(len(ob_trips) != 0):
    <p>Outbound - {{len(ob_trips)}} Trips</p>
  
    % include('templates/triplist', triplist=ob_trips)
  % end

  % if(len(ib_trips) != 0):
    <p>Inbound - {{len(ib_trips)}} Trips</p>
  
    % include('templates/triplist', triplist=ib_trips)
  % end
% end

% include('templates/footer')
