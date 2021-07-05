% import json
% import server

% rebase('base', title='Map', include_maps=True)

% if len(buses) == 0:
  % if system is not None and not system.supports_realtime:
    <h1>Map</h1>
    <hr />

    <p>
      {{ system }} does not currently support realtime. Please choose a different system.
    </p>

    % include('components/systems', realtime_only=True)
  % else:
    % if system is None:
      There are no buses out right now.
      BC Transit does not have late night service, so this should be the case overnight.
      If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.
      Please check back later!
    % else:
      <p>
        There are no buses out in {{ system }} right now. Please choose a different system.
      </p>

      % include('components/systems', realtime_only=True)
    % end
  % end
% else:
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
      if (bus.number === "Unknown Bus") {
        marker.className = "marker";
        marker.innerHTML = "<img src=\"/img/bus.png\" /><div><span>" + bus.number + "</span></div>";
      } else {
        marker.className = "marker linking";
        marker.innerHTML = "<a href=\"/bus/" + bus.number +"\"><img src=\"/img/bus.png\" /><div><span>" + bus.number + "</span></div></a>";
      }
  
      lons.push(bus.lon)
      lats.push(bus.lat)
  
      new mapboxgl.Marker(marker).setLngLat([bus.lon, bus.lat]).addTo(map);
    }
  
    if (lons.length === 1 && lats.length === 1) {
      map.jumpTo({
        center: [lons[0], lats[0]],
        zoom: 14
      })
    } else {
      const minLon = Math.min.apply(Math, lons)
      const maxLon = Math.max.apply(Math, lons)
      const minLat = Math.min.apply(Math, lats)
      const maxLat = Math.max.apply(Math, lats)
      map.fitBounds([[minLon, minLat], [maxLon, maxLat]], {
        duration: 0,
        padding: {top: 200, bottom: 100, left: 100, right: 100}
      })
    }
  </script>
% end
