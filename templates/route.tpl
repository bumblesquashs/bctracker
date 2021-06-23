% from models.trip import Direction

% rebase('base', title=str(route))

<h1>{{ route }}</h1>
<hr />

% outbound_trips = [t for t in route.trips if t.direction == Direction.OUTBOUND]
% inbound_trips = [t for t in route.trips if t.direction == Direction.INBOUND]

% has_outbound_trips = len(outbound_trips) > 0
% has_inbound_trips = len(inbound_trips) > 0

<div class="body list-container">
  % if len(route.services) > 1:
    <div class="list-navigation">
      % for service in route.services:
        <a href="#{{service}}" class='button'>{{ service }}</a>
      % end
    </div>
    <br />
  % end

  % for service in route.services:
    % service_outbound_trips = [t for t in outbound_trips if t.service == service]
    % service_inbound_trips = [t for t in inbound_trips if t.service == service]
    <div class="list-content">
      <h2 class="list-content-title" id="{{service}}">{{ service }}</h2>
      <div class="list-content-subtitle">{{ service.date_string }}</div>
      <div class="list-container">
        % if len(inbound_trips) > 0:
          <div class="list-content">
            % if len(service_outbound_trips) > 0:
              <h3>Inbound</h3>
            % end
            % include('components/service_trips', trips=service_inbound_trips)
          </div>
        % end

        % if len(service_outbound_trips) > 0:
          <div class="list-content">
            % if len(service_inbound_trips) > 0:
              <h3>Outbound</h3>
            % end
            % include('components/service_trips', trips=service_outbound_trips)
          </div>
        % end
      </div>
    </div>
  % end
</div>
