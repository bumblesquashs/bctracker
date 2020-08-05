% import datastructure as ds

% include('templates/header', title='Bus Stop {0}'.format(stop.stopcode), include_maps=True)

<h1>{{ stop.stopname }}</h1>
<h2>Bus Stop {{ stop.stopcode }}</h2>
<hr />

% include('templates/map', lon=stop.stoplon, lat=stop.stoplat)

% for day_str in day_order:
  % include('templates/stop_day', day=day_str, stop_entries=day_entries[day_str])
% end

% include('templates/footer')
