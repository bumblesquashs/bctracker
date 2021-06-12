% rebase('base', title=str(stop), include_maps=True)

<h1>{{ stop }}</h1>
<h2>Bus Stop {{ stop.number }}</h2>
<hr />

% include('components/map', lon=stop.lon, lat=stop.lat, marker_type='stop')

<p>
  % for service in stop.services:
    <a href="#{{service}}" class="button spaced-button">{{ service }}</a>
  % end
</p>

% for service in stop.services:
  % stop_times = [stop_time for stop_time in stop.stop_times if stop_time.trip.service == service]
  % include('components/stop_day', service=service, stop_times=stop_times)
% end
