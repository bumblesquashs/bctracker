% import json

% position = bus.position

<div id="map"></div>
<script>
    const lat = parseFloat("{{position.lat}}");
    const lon = parseFloat("{{position.lon}}");
    
    const map = new mapboxgl.Map({
        container: 'map',
        center: [lon, lat],
        zoom: 14,
        style: prefersDarkScheme ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v10',
        interactive: false
    });
</script>

% trip = position.trip
% if trip is not None:
    <script>
        const points = JSON.parse('{{! json.dumps([p.json_data for p in trip.points]) }}');
        
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
    
    % stops = {d.stop for d in trip.departures}
    <script>
        const stops = JSON.parse('{{! json.dumps([s.json_data for s in stops]) }}');
        
        for (const stop of stops) {
            const element = document.createElement('div');
            element.className = 'marker small';
            element.innerHTML = "\
                <div class='link'></div>\
                <a href=\"{{get_url(trip.system)}}/stops/" + stop.number +"\">\
                    <img src=\"/img/stop.png\" />\
                    <div class='title'><span>" + stop.number + "</span></div>\
                    <div class='subtitle'><span>" + stop.name + "</span></div>\
                </a>";
            element.style.backgroundColor = "#{{trip.route.colour}}";
            
            new mapboxgl.Marker(element).setLngLat([stop.lon, stop.lat]).addTo(map);
        }
    </script>
% end

<script>
    const element = document.createElement('div');
    element.className = 'marker';
    element.innerHTML = '<img src="/img/bus.png" />'
    element.style.backgroundColor = "#{{bus.colour}}";
    
    new mapboxgl.Marker(element).setLngLat([lon, lat]).addTo(map);
</script>
