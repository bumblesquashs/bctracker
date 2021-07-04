% import server
% import json

<div id="map"></div>
<script>
  const lat = parseFloat("{{stop.lat}}");
  const lon = parseFloat("{{stop.lon}}");

  mapboxgl.accessToken = '{{server.mapbox_api_key}}';
  var map = new mapboxgl.Map({
    container: 'map',
    center: [lon, lat],
    zoom: 14,
    style: 'mapbox://styles/mapbox/streets-v11',
    interactive: false
  });

  map.setStyle('mapbox://styles/mapbox/light-v10')

  var marker = document.createElement('div');
  marker.className = 'marker';
  marker.innerHTML = '<img src="/img/stop.png" />'

  new mapboxgl.Marker(marker).setLngLat([lon, lat]).addTo(map);
</script>
