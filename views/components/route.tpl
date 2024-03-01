% if route is not None:
    % if type(route) == str:
        <span class="route">{{ route }}</span>
    % else:
        <span class="tooltip-anchor">
            % if get('include_link', False):
                <a class="route" style="background-color: #{{ route.colour }};" href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route.number }}</a>
            % else:
                <span class="route" style="background-color: #{{ route.colour }};">{{ route.number }}</span>
            % end
            % if get('include_tooltip', False):
                <div class="tooltip right">{{ route }}</div>
            % end
        </span>
    % end
% end
