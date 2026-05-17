<div class="route-list">
    % for route in sorted([r for r in routes if r]):
        % include('components/route', include_link=True, include_tooltip=True, compact=True)
    % end
</div>
