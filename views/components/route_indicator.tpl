% if route is not None:
    <span class="tooltip-anchor">
        % if get('include_link', False):
            <a class="route-number" style="background-color: #{{ route.colour }};" href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route.number }}</a>
        % else:
            <span class="route-number" style="background-color: #{{ route.colour }};">{{ route.number }}</span>
        % end
        % if get('include_tooltip', False):
            <div class="tooltip">
                <div class="title">{{ route }}</div>
            </div>
        % end
    </span>
% end
