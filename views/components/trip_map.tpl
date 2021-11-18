% import json

<div id="map"></div>
<a href="{{ get_url(system, f'trips/{trip.id}/map') }}" class="button">Show Full Map</a>

<script>
    const points = JSON.parse('{{! json.dumps([p.json_data for p in trip.points]) }}')
    
    const map = new mapboxgl.Map({
        container: 'map',
        center: [0, 0],
        zoom: 1,
        style: prefersDarkScheme ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v10',
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

% for position in trip.positions:
    <script>
        map.on('load', function() {
            const bus = JSON.parse('{{! json.dumps(position.bus.json_data) }}');
            
            const element = document.createElement("div");
            element.className = "marker";
            if (bus.number < 0) {
                element.innerHTML = "\
                    <span>\
                        <img src=\"/img/bus.png\" />\
                        <div class='title'><span>Unknown Bus</span></div>\
                    </span>";
            } else {
                element.innerHTML = "\
                    <div class='link'></div>\
                    <a href=\"/bus/" + bus.number +"\">\
                        <img src=\"/img/bus.png\" />\
                        <div class='title'><span>" + bus.number + "</span></div>\
                    </a>";
            }
            element.style.backgroundColor = "#" + bus.colour;
        
            new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map);
        })
    </script>
% end
