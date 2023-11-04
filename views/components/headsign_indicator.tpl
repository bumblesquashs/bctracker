% if trip is not None and trip.route is not None:
    <div class="flex-row flex-gap-5">
        <div class="route-line" style="background-color: #{{ trip.route.colour }}"></div>
        <div class="flex-1">{{ trip }}</div>
    </div>
% end
