<div class="route-indicator">
    % for route in routes:
        <span class="route-number" style="background-color: #{{ route.colour }};">{{ route.number }}</span>
    % end
</div>
