<div class="vehicle">
    % if vehicle.is_known and get('enable_link', True):
        % if context.realtime_enabled:
            <a href="{{ context.url('bus', vehicle) }}">{{ vehicle }}</a>
        % else:
            % from models.context import Context
            <a href="{{ Context().url('bus', vehicle) }}">{{ vehicle }}</a>
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
