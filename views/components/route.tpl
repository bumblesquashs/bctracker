% if route is not None:
    <div class="route tooltip-anchor">
        % if type(route) == str:
            <span class="route-number">{{ route }}</span>
        % else:
            % if get('include_link', False):
                <a class="route-number" style="background-color: #{{ route.colour }};" href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route.number }}</a>
            % else:
                <span class="route-number" style="background-color: #{{ route.colour }};">{{ route.number }}</span>
            % end
            % if get('include_tooltip', False):
                <div class="tooltip">{{ route }}</div>
            % end
        % end
    </div>
% end
