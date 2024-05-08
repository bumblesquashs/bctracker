% if trip and trip.route:
    <div class="headsign">
        <div class="route-line" style="background-color: #{{ trip.route.colour }}"></div>
        <div>{{ trip }}</div>
    </div>
% end
