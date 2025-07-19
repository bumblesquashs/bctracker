<div class="route-list">
    % for route in routes:
        % include('components/route', include_link=True, include_tooltip=True, compact=True)
    % end
</div>
