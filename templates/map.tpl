% import json
% import server

% rebase('base', title='Map', include_maps=True)

<div class="system-map-header">
  <h1>Map</h1>
</div>

<div id="system-map"></div>

<script>
  mapboxgl.accessToken = "{{server.mapbox_api_key}}";
  var map = new mapboxgl.Map({
    container: "system-map",
    center: [0, 0],
    zoom: 1,
    style: "mapbox://styles/mapbox/streets-v11"
  });
  map.setStyle("mapbox://styles/mapbox/light-v10");

  const buses = JSON.parse('{{! json.dumps([b.json_data for b in buses if b.position.has_location]) }}');

  var lons = []
  var lats = []
  
  for (var bus of buses) {
    var marker = document.createElement("div");
    marker.className = "marker";
    marker.innerHTML = "<img src=\"/img/bus.png\" /><div><span>" + bus.number + "</span></div>";

    lons.push(bus.lon)
    lats.push(bus.lat)

    new mapboxgl.Marker(marker).setLngLat([bus.lon, bus.lat]).addTo(map);
  }

  const minLon = Math.min.apply(Math, lons)
  const maxLon = Math.max.apply(Math, lons)
  const minLat = Math.min.apply(Math, lats)
  const maxLat = Math.max.apply(Math, lats)
  map.fitBounds([[minLon, minLat], [maxLon, maxLat]], {
    duration: 0,
    padding: {top: 200, bottom: 100, left: 100, right: 100}
  })
</script>