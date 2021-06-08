% from models.trip import Direction

% include('components/header', title=str(route))

<h1>{{ route }}</h1>
<hr />

<p>
  % for service in sorted(route.services):
    <a href="#{{service}}" class='button spaced-button'>{{ service }}</a>
  % end
</p>

% for service in sorted(route.services):
  % trips = [trip for trip in route.trips if trip.service == service]

  <h2 id="{{service}}">{{ service }}</h2>

  % outbound_trips = [trip for trip in trips if trip.direction == Direction.OUTBOUND]
  % if len(outbound_trips) > 0:
    <p>Outbound - {{ len(outbound_trips) }} trips</p>

    % include('components/route_trips', trips=outbound_trips)
  % end

  % inbound_trips = [trip for trip in trips if trip.direction == Direction.INBOUND]
  % if len(inbound_trips) > 0:
    <p>Inbound - {{ len(inbound_trips) }} trips</p>

    % include('components/route_trips', trips=inbound_trips)
  % end
% end

% include('components/footer')
