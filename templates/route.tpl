% from models.trip import Direction

% rebase('base', title=str(route))

<h1>{{ route }}</h1>
<hr />

<div class="side-menu">
  <div class="info-box">
    <div class="info-box-header">
      <h3>Route Details</h3>
    </div>
    <div class="info-box-content">
      <div class="info-box-row">
        <span class="info-box-name">First trip outbound</span>
        <div class="info-box-value">
          % for service in route.services:
            % trips = [t for t in route.trips if t.service == service and t.direction == Direction.OUTBOUND]
            % if len(trips):
              <span>{{ service }} - {{ trips[0].start_time }}</span>
              <br />
            % end
          % end
        </div>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">First trip inbound</span>
        <div class="info-box-value">
          % for service in route.services:
            % trips = [t for t in route.trips if t.service == service and t.direction == Direction.INBOUND]
            % if len(trips) > 0:
              <span>{{ service }} - {{ trips[0].start_time }}</span>
              <br />
            % end
          % end
        </div>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Last trip outbound</span>
        <div class="info-box-value">
          % for service in route.services:
            % trips = [t for t in route.trips if t.service == service and t.direction == Direction.OUTBOUND]
            % if len(trips) > 0:
              <span>{{ service }} - {{ trips[-1].end_time }}</span>
              <br />
            % end
          % end
        </div>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Last trip inbound</span>
        <div class="info-box-value">
          % for service in route.services:
            % trips = [t for t in route.trips if t.service == service and t.direction == Direction.INBOUND]
            % if len(trips) > 0:
              <span>{{ service }} - {{ trips[-1].end_time }}</span>
              <br />
            % end
          % end
        </div>
        <br style="clear: both;" />
      </div>
    </div>
  </div>
</div>

<div class="list-container">
  <div class="list-navigation">
    % for service in route.services:
      <a href="#{{service}}" class='button'>{{ service }}</a>
    % end
  </div>
  <br />

  % for service in route.services:
    <div class="list-content">
      % trips = [trip for trip in route.trips if trip.service == service]
  
      <h2 id="{{service}}">{{ service }}</h2>
  
      % outbound_trips = [trip for trip in trips if trip.direction == Direction.OUTBOUND]
      % if len(outbound_trips) > 0:
        <p>Outbound</p>
        % include('components/service_trips', trips=outbound_trips)
      % end
  
      % inbound_trips = [trip for trip in trips if trip.direction == Direction.INBOUND]
      % if len(inbound_trips) > 0:
        <p>Inbound</p>
        % include('components/service_trips', trips=inbound_trips)
      % end
    </div>
  % end
</div>
