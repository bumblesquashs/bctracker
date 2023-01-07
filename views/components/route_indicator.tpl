<div class="route-indicator">
    % for route in routes:
        % if type(route) == str:
            <span class="route-number">{{ route }}</span>
        % else:
            <span class="route-number" style="background-color: #{{ route.colour }};">{{ route.number }}</span>
        % end
    % end
</div>
