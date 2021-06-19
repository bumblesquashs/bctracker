% rebase('base', title=str(trip), include_maps=True)

<h1>{{ trip }}</h1>
<h2>Trip {{ trip.id }}</h2>
<hr />

<div class="sidebar">
  % include('components/trip_map', trip=trip)
  
  <div class="info-box">
    <div class="info-box-section">
      % include('components/service_indicator', service=trip.service)
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Start time</div>
      <div class="info-box-value">{{ trip.start_time }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">End time</div>
      <div class="info-box-value">{{ trip.end_time }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Number of stops</div>
      <div class="info-box-value">{{ len(trip.stop_times) }}</div>
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
  </div>
</div>

<div class="body">
  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th>Time</th>
        <th class="desktop-only">Stop Number</th>
        <th class="desktop-only">Stop Name</th>
        <th class="mobile-only">Stop</th>
      </tr>
    </thead>
    <tbody>
      % for stop_time in trip.stop_times:
        <tr>
          <td>{{ stop_time.time }}</td>
          <td>
            <a href="{{ get_url(stop_time.system, f'stops/{stop_time.stop.number}') }}">{{ stop_time.stop.number }}</a>
            <span class="mobile-only smaller-font">
              <br />
              {{ stop_time.stop }}
            </span>
          </td>
          <td class="desktop-only">{{ stop_time.stop }}</td>
        </tr>
      % end
    </tbody>
  </table>
</div>
