% import datastructure as ds

<div id="map"></div>
<script>
    const lat = parseFloat("{{lat}}");
    const lon = parseFloat("{{lon}}");

    mapboxgl.accessToken = ''; // Replace with proper token in production and when testing - DO NOT COMMIT!
    var map = new mapboxgl.Map({
      container: 'map',
      center: [lon, lat],
      zoom: 14,
      style: 'mapbox://styles/mapbox/streets-v11',
      interactive: false
    });

    var marker = document.createElement('div');
    marker.className = 'marker';

    new mapboxgl.Marker(marker).setLngLat([lon, lat]).addTo(map);

    map.setStyle('mapbox://styles/mapbox/light-v10')
</script>

% if defined('shape_id'):
  % points = filter(lambda p: p.shape_id == shape_id, ds.all_points)
  % sorted_points = sorted(points, key=lambda p: int(p.sequence))
  % coords = list(map(lambda p: [float(p.lon), float(p.lat)], sorted_points))
  <script>
    const coords = {{ coords }}

    map.on('load', function() {
      map.addSource('route', {
        'type': 'geojson',
        'data': {
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'LineString',
            'coordinates': coords
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
          'line-color': '#AAAAAA',
          'line-width': 4
        }
      });
    });
  </script>
% end