<div class="route-indicator">
    % for route in routes:
        % if type(route) == str:
            <span class="route-number">{{ route }}</span>
        % else:
            % include('components/route_indicator', include_link=True, include_tooltip=True)
        % end
    % end
</div>
