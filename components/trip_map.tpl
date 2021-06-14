% import server

% coords = list(map(lambda p: [float(p.lon), float(p.lat)], trip.points))

<div id="map"></div>
<script>
  const coords = {{ coords }}

  minLon = coords[0][0]
  maxLon = coords[0][0]

  minLat = coords[0][1]
  maxLat = coords[0][1]

  console.log(minLon, maxLon, minLat, maxLat)

  for (const coord of coords) {
    console.log(coord)
    let lon = coord[0]
    let lat = coord[1]
    console.log(lon, lat)
    if (lon < minLon) {
      minLon = lon
    }
    if (lon > maxLon) {
      maxLon = lon
    }

    if (lat < minLat) {
      minLat = lat
    }
    if (lat > maxLat) {
      maxLat = lat
    }
  }

  console.log(minLon, maxLon, minLat, maxLat)

  mapboxgl.accessToken = '{{server.mapbox_api_key}}';
  var map = new mapboxgl.Map({
    container: 'map',
    center: [(minLon + maxLon) / 2, (minLat + maxLat) / 2],
    zoom: 14,
    style: 'mapbox://styles/mapbox/streets-v11',
    interactive: false
  });

  map.setStyle('mapbox://styles/mapbox/light-v10')

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
        'line-color': '#4040FF',
        'line-width': 4
      }
    });
    map.fitBounds([[minLon, minLat], [maxLon, maxLat]], {
      duration: 0,
      padding: 20
    })
  });
</script>