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
    % last_hour = -1
    % for trip in trips:
      % this_hour = int(trip.start_time.split(':')[0])
      % if last_hour == -1:
        % last_hour = this_hour
      % elif this_hour > last_hour:
        <tr>
          <td class="desktop-only" colspan="5"><hr /></td>
          <td class="mobile-only" colspan="3"><hr /></td>
        </tr>
        % last_hour = this_hour
      % end
      <tr>
        <td>{{ trip.start_time }}</td>
        <td>{{ trip }}</td>
        <td class="desktop-only">
          <a href="{{ get_url(trip.stop_times[0].stop.system.id, f'stops/{trip.stop_times[0].stop.number}') }}">
            {{ trip.stop_times[0].stop }}
          </a>
        </td>
        <td class="desktop-only">
          <a href="{{ get_url(trip.block.system.id, f'blocks/{trip.block.id}') }}">
            {{ trip.block.id }}
          </a>
        </td>
        <td>
          <a href="{{ get_url(trip.system.id, f'trips/{trip.id}') }}">
            {{ trip.id }}
          </a>
        </td>
      </tr>
    %end
  </tbody>
</table>
