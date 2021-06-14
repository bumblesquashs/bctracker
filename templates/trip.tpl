% rebase('base', title=str(trip))

<h1>{{ trip }}</h1>
<h2>Trip {{ trip.id }} ({{ trip.service }})</h2>
<hr />

<p>
  <a href="{{ get_url(trip.system.id, f'routes/{trip.route.number}') }}">View Route</a>
  <br />
  <a href="{{ get_url(trip.block.system.id, f'blocks/{trip.block.id}') }}">View Block</a>
</p>

<p>Number of stops: {{ len(trip.stop_times) }}</p>

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
