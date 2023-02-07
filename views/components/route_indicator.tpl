<div class="route-indicator">
    % for route in routes:
        % if type(route) == str:
            <span class="route-number">{{ route }}</span>
        % else:
            <span class="tooltip-anchor">
                <a class="route-number" style="background-color: #{{ route.colour }};" href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route.number }}</a>
                <div class="tooltip">
                    <div class="title">{{ route.number }} {{! route.display_name }}</div>
                </div>
            </span>
        % end
    % end
</div>
