<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th class="desktop-only">Start Time</th>
      <th class="mobile-only">Start</th>
      <th>Headsign</th>
      <th class="desktop-only">Departing From</th>
      <th class="desktop-only">Block</th>
      <th>Trip</th>
    </tr>
  </thead>
  <tbody>
    % for trip in trips:
      % first_stop = trip.stop_times[0].stop
      <tr>
        <td>{{ trip.start_time }}</td>
        <td>{{ trip }}</td>
        <td class="desktop-only"><a href="{{ get_url(first_stop.system.id, f'stops/{first_stop.number}') }}">{{ first_stop }}</a></td>
        <td class="desktop-only"><a href="{{ get_url(trip.block.system.id, f'blocks/{trip.block.id}') }}">{{ trip.block.id }}</a></td>
        <td><a href="{{ get_url(trip.system.id, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
      </tr>
    %end
  </tbody>
</table>
