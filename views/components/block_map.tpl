% import json

<div id="map"></div>
<script>
    const map = new mapboxgl.Map({
        container: 'map',
        center: [0, 0],
        zoom: 1,
        style: prefersDarkScheme ? 'mapbox://styles/mapbox/dark-v10' : 'mapbox://styles/mapbox/light-v10',
        interactive: false
    });
    
    const lons = [];
    const lats = [];
</script>

% shape_ids = {(t.shape_id, t.route.colour) for t in block.get_trips(sheet)}
% for (shape_id, colour) in shape_ids:
    % points = sorted(block.system.get_shape(shape_id).points)
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
                    'line-color': '#{{colour}}',
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
            padding: 20
        })
    })
</script>

% for position in block.positions:
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
                        <div class='subtitle'><span>" + bus.headsign + "</span></div>\
                    </span>";
            } else {
                element.innerHTML = "\
                    <div class='link'></div>\
                    <a href=\"/bus/" + bus.number +"\">\
                        <img src=\"/img/bus.png\" />\
                        <div class='title'><span>" + bus.number + "</span></div>\
                        <div class='subtitle'><span>" + bus.headsign + "</span></div>\
                    </a>";
            }
            element.style.backgroundColor = "#" + bus.colour;
        
            new mapboxgl.Marker(element).setLngLat([bus.lon, bus.lat]).addTo(map);
        })
    </script>
% end
