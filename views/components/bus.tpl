<div class="bus">
    % if bus.is_known and get('enable_link', True):
        % if context.system:
            <a href="{{ get_url(bus.context, 'bus', bus) }}">{{ bus }}</a>
        % else:
            <a href="{{ get_url(bus.context, 'bus', bus.context.agency, bus) }}">{{ bus }}</a>
        % end
    % else:
        <div>{{ bus }}</div>
    % end
    % decoration = bus.find_decoration()
    % if decoration and decoration.enabled:
        <div class="decoration tooltip-anchor">
            {{ decoration }}
            % if decoration.description:
                <div class="tooltip right">{{ decoration.description }}</div>
            % end
        </div>
    % end
</div>
