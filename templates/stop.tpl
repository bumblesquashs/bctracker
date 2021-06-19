% rebase('base', title=str(stop), include_maps=True)

<h1>{{ stop }}</h1>
<h2>Bus Stop {{ stop.number }}</h2>
<hr />

<div class="sidebar">
  % include('components/map', lon=stop.lon, lat=stop.lat, marker_type='stop')
  
  <div class="info-box">
    <div class="info-box-section">
      % include('components/service_indicator', services=stop.services)
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Route{{ '' if len(stop.routes) == 1 else 's' }}</div>
      <div class="info-box-value">
        % for route in stop.routes:
          <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
          <br />
        % end
      </div>
    </div>
  </div>
</div>

<div class="body list-container">
  % if len(stop.services) > 0:
    <div class="list-navigation">
      % for service in stop.services:
        <a href="#{{service}}" class="button">{{ service }}</a>
      % end
    </div>
    <br />
  % end

  % for service in stop.services:
    % stop_times = [stop_time for stop_time in stop.stop_times if stop_time.trip.service == service]

    % if len(stop_times) > 0:
      <div class="list-content">
        <h2 id="{{service}}">{{ service }}</h2>
        
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
              % block = stop_time.trip.block
              % this_hour = int(stop_time.time.split(':')[0])
              % if last_hour == -1:
                % last_hour = this_hour
              % end
              <tr class="{{'hourly' if this_hour > last_hour else ''}}">
                <td>{{ stop_time.time }}</td>
                <td>{{ stop_time.trip }}</td>
                <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                <td><a href="{{ get_url(stop_time.trip.system, f'trips/{stop_time.trip.id}') }}">{{ stop_time.trip.id }}</a></td>
              </tr>
              % if this_hour > last_hour:
                % last_hour = this_hour
              % end
            % end
          </tbody>
        </table>
      </div>
    % end
  % end
</div>