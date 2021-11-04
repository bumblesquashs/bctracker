% import json

% rebase('base', title=f'{route} - Map', include_maps=True)

<div class="page-header map-page">
    <h1 class="title">{{ route }} - Map</h1>
    <a href="{{ get_url(system, f'routes/{route.number}') }}">Return to route overview</a>
</div>

<div id="full-map"></div>

<script>
    const map = new mapboxgl.Map({
        container: 'full-map',
        center: [0, 0],
        zoom: 1,
        style: prefersDarkScheme ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v10',
    });
    
    const lons = [];
    const lats = [];
</script>

% trips = route.get_trips(sheet)
% shape_ids = {t.shape_id for t in trips}
% for shape_id in shape_ids:
    % points = sorted(route.system.get_shape(shape_id).points)
    <script>
        map.on('load', function() {
            const points = JSON.parse('{{! json.dumps([p.json_data for p in points]) }}');
            
            map.addSource('{{shape_id}}', {
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
                'id': '{{shape_id}}',
                'type': 'line',
                'source': '{{shape_id}}',
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': '#{{route.colour}}',
                    'line-width': 4
                }
            });
            
            for (point of points) {
                lons.push(point.lon);
                lats.push(point.lat);
            }
        });
    </script>
% end

<script>
    map.on('load', function() {
        const minLon = Math.min.apply(Math, lons)
        const maxLon = Math.max.apply(Math, lons)
        const minLat = Math.min.apply(Math, lats)
        const maxLat = Math.max.apply(Math, lats)
        map.fitBounds([[minLon, minLat], [maxLon, maxLat]], {
            duration: 0,
            padding: {top: 200, bottom: 100, left: 100, right: 100}
        })
    })
</script>

% stops = {d.stop for t in trips for d in t.departures}
<script>
    const stops = JSON.parse('{{! json.dumps([s.json_data for s in stops]) }}');
    
    for (const stop of stops) {
        const element = document.createElement('div');
        element.className = 'marker small';
        element.innerHTML = "\
            <div class='link'></div>\
            <a href=\"{{get_url(route.system)}}/stops/" + stop.number +"\">\
                <img src=\"/img/stop.png\" />\
                <div class='title'><span>" + stop.number + "</span></div>\
                <div class='subtitle'><span>" + stop.name + "</span></div>\
            </a>";
        element.style.backgroundColor = "#{{route.colour}}";
        
        new mapboxgl.Marker(element).setLngLat([stop.lon, stop.lat]).addTo(map);
    }
</script>

% for position in route.positions:
    <script>
        map.on('load', function() {
            const bus = JSON.parse('{{! json.dumps(position.bus.json_data) }}');
            
            const element = document.createElement("div");
            element.className = "marker";
            element.innerHTML = "\
                <div class='link'></div>\
                <a href=\"/bus/" + bus.number +"\">\
                    <img src=\"/img/bus.png\" />\
                    <div class='title'><span>" + bus.number + "</span></div>\
                    <div class='subtitle'><span>" + bus.headsign + "</span></div>\
                </a>";
            element.style.backgroundColor = "#" + bus.colour;
        
            new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map);
        })
    </script>
% end
