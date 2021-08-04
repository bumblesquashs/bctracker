% import json

% position = bus.position

<div id="map"></div>
<script>
  const lat = parseFloat("{{position.lat}}");
  const lon = parseFloat("{{position.lon}}");

  mapboxgl.accessToken = '{{mapbox_api_key}}';
  var map = new mapboxgl.Map({
    container: 'map',
    center: [lon, lat],
    zoom: 14,
    style: 'mapbox://styles/mapbox/light-v10',
    interactive: false
  });

  var marker = document.createElement('div');
  marker.className = 'marker';
  marker.innerHTML = '<img src="/img/bus.png" />'
  marker.style.backgroundColor = "#{{bus.colour}}";

  new mapboxgl.Marker(marker).setLngLat([lon, lat]).addTo(map);
</script>

% trip = position.trip
% if trip is not None:
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
          'line-color': '#{{trip.route.colour}}',
          'line-width': 4
        }
      });
    });
  </script>
% end
