<div class="flex-row flex-gap-5">
    % if bus.is_known and get('enable_link', True):
        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
    % else:
        <div>{{ bus }}</div>
    % end
    % icon = bus.icon
    % if icon is not None and icon.enabled:
        <div class="icon tooltip-anchor">
            {{ icon }}
            % if icon.description is not None:
                <div class="tooltip">{{ icon.description }}</div>
            % end
        </div>
    % end
</div>
