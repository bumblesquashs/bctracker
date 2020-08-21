% import datastructure as ds

% include('templates/header', title=stop.stopname, include_maps=True)

<h1>{{ stop.stopname }}</h1>
<h2>Bus Stop {{ stop.stopcode }}</h2>
<hr />

% include('templates/map', lon=stop.stoplon, lat=stop.stoplat, marker_type='stop')

<p>
  % for day_str in day_order:
    <a href="#{{day_str}}" class="button spaced-button">{{ day_str }}</a>
  % end
</p>

% for day_str in day_order:
  % include('templates/stop_day', day=day_str, stop_entries=day_entries[day_str])
% end

% include('templates/footer')
