<div class="bus">
    % if bus.is_known and get('enable_link', True):
        <a class="number" href="{{ get_url(context, 'bus', bus) }}">{{ bus }}</a>
    % else:
        <div class="number">{{ bus }}</div>
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
