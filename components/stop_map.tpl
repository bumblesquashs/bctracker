% import json

<div id="map"></div>
<script>
  const lat = parseFloat("{{stop.lat}}");
  const lon = parseFloat("{{stop.lon}}");

  mapboxgl.accessToken = '{{mapbox_api_key}}';
  var map = new mapboxgl.Map({
    container: 'map',
    center: [lon, lat],
    zoom: 14,
    style: prefersDarkScheme ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v10',
    interactive: false
  });

  var marker = document.createElement('div');
  marker.className = 'marker';
  marker.innerHTML = '<img src="/img/stop.png" />'

  new mapboxgl.Marker(marker).setLngLat([lon, lat]).addTo(map);
</script>
