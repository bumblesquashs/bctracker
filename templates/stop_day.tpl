% if len(stop_entries) > 0:
  <h2>{{ day }} ({{ len(stop_entries) }} Trips)</h2>

  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th>Time</th>
        <th>Headsign</th>
        <th>Block</th>
        <th>Trip</th>
      </tr>
    </thead>
    <tbody>
      % last_hour = -1
      % for stop_entry in stop_entries:
        % this_hour = int(stop_entry.stoptime.split(':')[0])
        % if last_hour == -1:
          % last_hour = this_hour
        % elif this_hour > last_hour:
          <tr>
            <td colspan="4"><hr /></td>
          </tr>
          % last_hour = this_hour
        % end
        <tr>
          <td>{{ stop_entry.stoptime }}</td>
          <td>{{ stop_entry.trip.headsign }}</td>
          <td><a href="/blocks/{{ stop_entry.trip.blockid }}">{{ stop_entry.trip.blockid }}</a></td>
          <td><a href="/blocks/{{ stop_entry.tripid }}">{{ stop_entry.tripid }}</a></td>
        </tr>
      % end
    </tbody>
  </table>
% end