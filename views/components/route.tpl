% if route:
    % compact = get('compact', False)
    % if type(route) == str:
        <span class="route {{ '' if compact else 'min-width' }}">{{ route }}</span>
    % else:
        <span class="tooltip-anchor">
            % if get('include_link', False):
                <a class="route {{ '' if compact else 'min-width' }}" style="background-color: #{{ route.colour }};" href="{{ get_url(route.context, 'routes', route) }}">{{ route.number }}</a>
            % else:
                <span class="route {{ '' if compact else 'min-width' }}" style="background-color: #{{ route.colour }};">{{ route.number }}</span>
            % end
            % if get('include_tooltip', False):
                <div class="tooltip right">{{ route }}</div>
            % end
        </span>
    % end
% end
