% import server
% import json

<div id="map"></div>
<script>
  const lat = parseFloat("{{lat}}");
  const lon = parseFloat("{{lon}}");

  mapboxgl.accessToken = '{{server.mapbox_api_key}}';
  var map = new mapboxgl.Map({
    container: 'map',
    center: [lon, lat],
    zoom: 14,
    style: 'mapbox://styles/mapbox/streets-v11',
    interactive: false
  });

  map.setStyle('mapbox://styles/mapbox/light-v10')
</script>

% if defined('marker_type'):
  % if marker_type == 'bus':
    <script>
      var marker = document.createElement('div');
      marker.className = 'marker';
      marker.innerHTML = '<img src="/img/bus.png" />'

      new mapboxgl.Marker(marker).setLngLat([lon, lat]).addTo(map);
    </script>
  % elif marker_type == 'stop':
    <script>
      var marker = document.createElement('div');
      marker.className = 'marker';
      marker.innerHTML = '<img src="/img/stop.png" />'

      new mapboxgl.Marker(marker).setLngLat([lon, lat]).addTo(map);
    </script>
  % end
% end

% if defined('trip'):
  <script>
    const points = JSON.parse('{{! json.dumps([p.json_data for p in trip.points]) }}')

    map.on('load', function() {
      map.addSource('route', {
        'type': 'geojson',
        'data': {
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'LineString',
            'coordinates': points.map(function (point) { return [point.lon, point.lat] })
          }
        }
      });
      map.addLayer({
        'id': 'route',
        'type': 'line',
        'source': 'route',
        'layout': {
          'line-join': 'round',
          'line-cap': 'round'
        },
        'paint': {
          'line-color': '#4040FF',
          'line-width': 4
        }
      });
    });
  </script>
% end
