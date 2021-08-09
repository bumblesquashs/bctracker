% import json

<div id="map"></div>
<script>
    const points = JSON.parse('{{! json.dumps([p.json_data for p in trip.points]) }}')
    
    mapboxgl.accessToken = '{{mapbox_api_key}}';
    const map = new mapboxgl.Map({
        container: 'map',
        center: [0, 0],
        zoom: 1,
        style: 'mapbox://styles/mapbox/light-v10',
        interactive: false
    });
    
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
        
        const lons = points.map(function (point) { return point.lon })
        const lats = points.map(function (point) { return point.lat })
        
        const minLon = Math.min.apply(Math, lons)
        const maxLon = Math.max.apply(Math, lons)
        const minLat = Math.min.apply(Math, lats)
        const maxLat = Math.max.apply(Math, lats)
        map.fitBounds([[minLon, minLat], [maxLon, maxLat]], {
            duration: 0,
            padding: 20
        })
    });
</script>