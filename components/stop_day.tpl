% if len(stop_times) > 0:
  <h2 id="{{service}}">{{ service }}</h2>
  <p>{{ len(stop_times) }} Trips</p>
  
  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th>Time</th>
        <th>Headsign</th>
        <th class="desktop-only">Block</th>
        <th>Trip</th>
      </tr>
    </thead>
    <tbody>
      % last_hour = -1
      % for stop_time in stop_times:
        % this_hour = int(stop_time.time.split(':')[0])
        % if last_hour == -1:
          % last_hour = this_hour
        % elif this_hour > last_hour:
          <tr>
            <td class="desktop-only" colspan="4"><hr /></td>
            <td class="mobile-only" colspan="3"><hr /></td>
          </tr>
          % last_hour = this_hour
        % end
        <tr>
          <td>{{ stop_time.time }}</td>
          <td>{{ stop_time.trip }}</td>
          <td class="desktop-only">
            <a href="{{ get_url(stop_time.trip.block.system.id, f'blocks/{stop_time.trip.block.id}') }}">
              {{ stop_time.trip.block.id }}
            </a>
          </td>
          <td>
            <a href="{{ get_url(stop_time.trip.system.id, f'trips/{stop_time.trip.id}') }}">
              {{ stop_time.trip.id }}
            </a>
          </td>
        </tr>
      % end
    </tbody>
  </table>
% end