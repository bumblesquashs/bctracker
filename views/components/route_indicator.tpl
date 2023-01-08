<div class="route-indicator">
    % for route in routes:
        % if type(route) == str:
            <span class="route-number">{{ route }}</span>
        % else:
            <a class="route-number" style="background-color: #{{ route.colour }};" href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route.number }}</a>
        % end
    % end
</div>
