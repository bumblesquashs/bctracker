% from formatting import format_date, format_date_mobile
% from models.bus_model import BusModelType

% rebase('base', title=f'Bus {bus}', include_maps=True)

<h1>Bus {{ bus }}</h1>
<hr />

<div class="sidebar">
  % position = bus.position
  % if not position.active:
    <div class="info-box">
      <h3 class="info-box-title">Not in service</h3>
    </div>
  % elif position.trip is None:
    % include('components/bus_map', bus=bus)

    <div class="info-box">
      <h3 class="info-box-title">Not in service</h3>
    </div>
  % else:
    % include('components/bus_map', bus=bus)

    % trip = position.trip
    <div class="info-box">
      <h3 class="info-box-title">{{ trip }}</h3>

      <div class="info-box-section">
        <div class="info-box-name">System</div>
        <div class="info-box-value">{{ trip.system }}</div>
      </div>
      <div class="info-box-section">
        <div class="info-box-name">Route</div>
        <div class="info-box-value">
          <a href="{{ get_url(trip.route.system, f'routes/{trip.route.number}') }}">{{ trip.route }}</a>
        </div>
      </div>
      <div class="info-box-section">
        <div class="info-box-name">Block</div>
        <div class="info-box-value">
          <a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a>
        </div>
      </div>
      <div class="info-box-section">
        <div class="info-box-name">Trip</div>
        <div class="info-box-value">
          <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
        </div>
      </div>
      % if position.stop is not None:
        % stop = position.stop
        <div class="info-box-section">
          <div class="info-box-name">Current Stop</div>
          <div class="info-box-value">
            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
          </div>
        </div>
      % end
    </div>
  % end
  
  <div class="info-box">
    % order = bus.order
    % model = bus.model
    <div class="info-box-section">
      <div class="info-box-name">Manufacturer</div>
      <div class="info-box-value">{{ model.manufacturer }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Model</div>
      <div class="info-box-value">{{ model.name }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Year</div>
      <div class="info-box-value">{{ order.year }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Vehicle Type</div>
      <div class="info-box-value">{{ model.type.value }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Length</div>
      <div class="info-box-value">{{ str(model.length).rstrip('0').rstrip('.') }} feet</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Fuel Type</div>
      <div class="info-box-value">{{ model.fuel }}</div>
    </div>
  </div>
</div>

<div class="body">
  % if len(history) == 0:
    <p>This bus doesn't have any recorded history.</p>
    <p>
      There are a few reasons why that might be the case:
      <ol>
        <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
        <li>It may not have been in service since BCTracker started recording bus history</li>
        <li>It may not have functional NextRide equipment installed</li>
        % if model.type == BusModelType.shuttle:
          <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
        % end
      </ol>
      Please check again later!
    </p>
  % else:
    <table class="pure-table pure-table-horizontal pure-table-striped">
      <thead>
        <tr>
          <th>Date</th>
          <th>System</th>
          <th class="desktop-only">Assigned Block</th>
          <th class="desktop-only">Assigned Routes</th>
          <th class="desktop-only">Start Time</th>
          <th class="desktop-only">End Time</th>
          <th class="mobile-only">Block</th>
        </tr>
      </thead>
      <tbody>
        % for block_history in history[:20]:
          <tr>
            <td class="desktop-only">{{ format_date(block_history.date) }}</td>
            <td class="mobile-only no-wrap">{{ format_date_mobile(block_history.date) }}</td>
            <td>{{ block_history.system }}</td>
            <td>
              % if block_history.is_available:
                % block = block_history.block
                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
              % else:
                <span>{{ block_history.block_id }}</span>
              % end
              <span class="mobile-only smaller-font">
                <br />
                {{ block_history.routes_string }}
              </span>
            </td>
            <td class="desktop-only">{{ block_history.routes_string }}</td>
            <td class="desktop-only">{{ block_history.start_time }}</td>
            <td class="desktop-only">{{ block_history.end_time }}</td>
          </tr>
        % end
      </tbody>
    </table>
  % end
</div>