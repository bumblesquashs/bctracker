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
        <div class="decoration tooltip-anchor">
            {{ decoration }}
            % if decoration.description:
                <div class="tooltip right">{{ decoration.description }}</div>
            % end
        </div>
    % end
</div>
