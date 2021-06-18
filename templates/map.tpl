% import server

% rebase('base', title='Map', include_maps=True)

<div class="system-map-header">
  <h1>Map</h1>
</div>

<div id="system-map"></div>

<script>
  mapboxgl.accessToken = '{{server.mapbox_api_key}}';
  var map = new mapboxgl.Map({
    container: 'system-map',
    center: [-123.538, 48.52],
    zoom: 9,
    style: 'mapbox://styles/mapbox/streets-v11'
  });
  map.setStyle('mapbox://styles/mapbox/light-v10')
</script>