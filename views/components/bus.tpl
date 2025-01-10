<div class="bus">
    % if bus.is_known and get('enable_link', True):
        <a href="{{ get_url(system, 'bus', bus) }}">{{ bus }}</a>
    % else:
        <div>{{ bus }}</div>
    % end
    % adornment = bus.find_adornment()
    % if adornment and adornment.enabled:
        <div class="adornment tooltip-anchor">
            {{ adornment }}
            % if adornment.description:
                <div class="tooltip right">{{ adornment.description }}</div>
            % end
        </div>
    % end
</div>
