% if get('departure') and departure.headsign:
    <div class="headsign">
        <div class="route-line" style="background-color: #{{ departure.trip.route.colour }}"></div>
        % headsign = str(departure)
        % if departure.context.config.enable_stacked_headsigns and '/' in headsign:
            % parts = headsign.split('/', 1)
            <div class="column">
                <div>{{ parts[0].strip() }}</div>
                <div class="smaller-font lighter-text">{{ parts[1].strip() }}</div>
            </div>
        % else:
            <div>{{ headsign }}</div>
        % end
    </div>
% elif trip and trip.route:
    % if trip.custom_headsigns:
        <div class="column">
            % for headsign in trip.custom_headsigns:
                <div class="headsign">
                    <div class="route-line" style="background-color: #{{ trip.route.colour }}"></div>
                    % if trip.context.config.enable_stacked_headsigns and '/' in headsign:
                        % parts = headsign.split('/', 1)
                        <div class="column">
                            <div>{{ parts[0].strip() }}</div>
                            <div class="smaller-font lighter-text">{{ parts[1].strip() }}</div>
                        </div>
                    % else:
                        <div>{{ headsign }}</div>
                    % end
                </div>
            % end
        </div>
    % else:
        <div class="headsign">
            <div class="route-line" style="background-color: #{{ trip.route.colour }}"></div>
            % headsign = str(trip)
            % if trip.context.config.enable_stacked_headsigns and '/' in headsign:
                % parts = headsign.split('/', 1)
                <div class="column">
                    <div>{{ parts[0].strip() }}</div>
                    <div class="smaller-font lighter-text">{{ parts[1].strip() }}</div>
                </div>
            % else:
                <div>{{ headsign }}</div>
            % end
        </div>
    % end
% end
