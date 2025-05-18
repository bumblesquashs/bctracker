% if stop:
    <div class="stop">
        % if get('show_name', True):
            % if get('include_link', True):
                <a class="stop-name {{ 'timing-point' if get('timepoint', False) else '' }}" href="{{ get_url(stop.context, 'stops', stop) }}">{{ stop }}</a>
            % else:
                <span class="stop-name {{ 'timing-point' if get('timepoint', False) else '' }}">{{ stop }}</span>
            % end
        % end
        % if get('show_number', True) and stop.context.show_stop_number:
            <div class="stop-number tooltip-anchor">
                {{ stop.number }}
                <div class="tooltip right">Stop code</div>
            </div>
        % end
    </div>
% else:
    <span class="lighter-text">Unavailable</span>
% end
