<div class="flex-row flex-gap-5">
    % if bus.is_known and get('enable_link', True):
        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
    % else:
        <div>{{ bus }}</div>
    % end
    % adornment = bus.adornment
    % if adornment is not None and adornment.enabled:
        <div class="adornment tooltip-anchor">
            {{ adornment }}
            % if adornment.description is not None:
                <div class="tooltip">{{ adornment.description }}</div>
            % end
        </div>
    % end
</div>
