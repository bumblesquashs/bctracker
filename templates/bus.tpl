
% rebase('base', title=f'Bus {bus}', include_maps=True)

<h1>Bus {{ bus }}</h1>
<h2>{{ bus.range }}</h2>
<hr />

<div class="sidebar">
  % if not bus.position.active:
    <h2>Not in service</h2>
  % elif bus.position.trip is None:
    % include('components/map', lat=bus.position.lat, lon=bus.position.lon, marker_type='bus')
    <h2>Not in service</h2>
  % else:
    % trip = bus.position.trip
    % include('components/map', lat=bus.position.lat, lon=bus.position.lon, marker_type='bus', trip=trip)
    <h2>{{ trip }}</h2>
    <div class="info-box">
      <div class="info-box-section">
        <div class="info-box-name">System</div>
        <div class="info-box-value">{{ trip.system }}</div>
      </div>
      <div class="info-box-section">
        <div class="info-box-name">Current Route</div>
        <div class="info-box-value">
          <a href="{{ get_url(trip.route.system, f'routes/{trip.route.number}') }}">{{ trip.route }}</a>
        </div>
      </div>
      <div class="info-box-section">
        <div class="info-box-name">Current Block</div>
        <div class="info-box-value">
          <a href="{{ get_url(trip.block.system, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a>
        </div>
      </div>
      <div class="info-box-section">
        <div class="info-box-name">Current Trip</div>
        <div class="info-box-value">
          <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
        </div>
      </div>
      % if bus.position.stop is not None:
        % stop = bus.position.stop
        <div class="info-box-section">
          <div class="info-box-name">Current Stop</div>
          <div class="info-box-value">
            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
          </div>
        </div>
      % end
    </div>
  % end
</div>

<div class="body">

</div>