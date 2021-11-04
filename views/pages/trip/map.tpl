% import json

% rebase('base', title=f'Trip {trip.id} - Map', include_maps=True)

<div class="page-header map-page">
    <h1 class="title">Trip {{ trip.id }} - Map</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <a href="{{ get_url(system, f'trips/{trip.id}') }}">Return to trip overview</a>
</div>

<div id="full-map"></div>

<script>
    const points = JSON.parse('{{! json.dumps([p.json_data for p in trip.points]) }}')
    
    const map = new mapboxgl.Map({
        container: 'full-map',
        center: [0, 0],
        zoom: 1,
        style: prefersDarkScheme ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v10'
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
            padding: {top: 200, bottom: 100, left: 100, right: 100}
        })
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

% for position in trip.positions:
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
                </a>";
            element.style.backgroundColor = "#" + bus.colour;
        
            new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map);
        })
    </script>
% end
