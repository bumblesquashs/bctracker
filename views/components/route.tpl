% if route is not None:
    % if type(route) == str:
        <div class="route">
            <div class="route-number">{{ route }}</div>
        </div>
    % else:
        <div class="route tooltip-anchor" style="background-color: #{{ route.colour }};">
            % if get('include_link', False):
                <a class="route-number" href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route.number }}</a>
            % else:
                <div class="route-number">{{ route.number }}</div>
            % end
            % if get('include_tooltip', False):
                <div class="tooltip">{{ route }}</div>
            % end
        </div>
    % end
% end
