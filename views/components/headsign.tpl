% if trip is not None and trip.route is not None:
    <div class="headsign">
        <div class="route-line" style="background-color: #{{ trip.route.colour }}"></div>
        <div>{{ trip }}</div>
    </div>
% end
