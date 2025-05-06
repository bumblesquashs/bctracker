% if get('departure') and departure.headsign:
    <div class="headsign">
        <div class="route-line" style="background-color: #{{ departure.trip.route.colour }}"></div>
        <div>{{ departure }}</div>
    </div>
% elif trip and trip.route:
    % if trip.custom_headsigns:
        <div class="column">
            % for headsign in trip.custom_headsigns:
                <div class="headsign">
                    <div class="route-line" style="background-color: #{{ trip.route.colour }}"></div>
                    <div>{{ headsign }}</div>
                </div>
            % end
        </div>
    % else:
        <div class="headsign">
            <div class="route-line" style="background-color: #{{ trip.route.colour }}"></div>
            <div>{{ trip }}</div>
        </div>
    % end
% end
