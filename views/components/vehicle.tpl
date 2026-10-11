<div class="vehicle">
    % if vehicle.is_known and get('enable_link', True):
        % if context.agency and context.agency == vehicle.agency:
            <a href="{{ context.url('fleet', vehicle) }}">{{ vehicle }}</a>
        % else:
            <a href="{{ vehicle.url() }}">{{ vehicle }}</a>
        % end
    % else:
        <div>{{ vehicle }}</div>
    % end
    % decoration = vehicle.find_decoration()
    % if decoration and decoration.enabled:
        % if decoration.website:
            <a class="decoration tooltip-anchor" href="{{ decoration.website }}", target="_blank">
                {{ decoration }}
                % if decoration.description:
                    <div class="tooltip right">
                        % if decoration.artist:
                            <div class="title">{{ decoration.description }}</div>
                            Designed by {{ decoration.artist }}
                        % else:
                            {{ decoration.description }}
                        % end
                        <i class="smaller-font">Click for more information</i>
                    </div>
                % end
            </a>
        % else:
            <div class="decoration tooltip-anchor">
                {{ decoration }}
                % if decoration.description:
                    <div class="tooltip right">
                        % if decoration.artist:
                            <div class="title">{{ decoration.description }}</div>
                            Designed by {{ decoration.artist }}
                        % else:
                            {{ decoration.description }}
                        % end
                    </div>
                % end
            </div>
        % end
    % end
</div>
