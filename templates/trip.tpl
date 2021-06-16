% rebase('base', title=str(trip), include_maps=True)

<h1>{{ trip }}</h1>
<h2>Trip {{ trip.id }}</h2>
<hr />

<div class="side-menu">
  % include('components/trip_map', trip=trip)
  
  <div class="info-box">
    <div class="info-box-header">
      <h3>Trip Details</h3>
    </div>
    <div class="info-box-content">
      <div class="info-box-row">
        <span class="info-box-name">Service day(s)</span>
        <span class="info-box-value">{{ trip.service }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Start time</span>
        <span class="info-box-value">{{ trip.start_time }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">End time</span>
        <span class="info-box-value">{{ trip.end_time }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Number of stops</span>
        <span class="info-box-value">{{ len(trip.stop_times) }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Route</span>
        <a class="info-box-value" href="{{ get_url(trip.system.id, f'routes/{trip.route.number}') }}">{{ trip.route }}</a>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Block</span>
        <a class="info-box-value" href="{{ get_url(trip.block.system.id, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a>
        <br style="clear: both;" />
      </div>
    </div>
  </div>
</div>

<div>
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
            <a href="{{ get_url(stop_time.system.id, f'stops/{stop_time.stop.number}') }}">{{ stop_time.stop.number }}</a>
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
