
% from models.weekday import Weekday

% url = get('url', None)
% url_suffix = get('url_suffix', '')
% compact = get('compact', False)

<div class="weekdays {{ 'compact' if compact else '' }}">
    % for weekday in Weekday:
        % name = weekday.abbreviation if compact else weekday.short_name
        % status = schedule.get_weekday_status(weekday)
        % if url is None or weekday not in schedule.weekdays:
            <span class="weekday {{ status }}">{{ name }}</span>
        % else:
            <a class="weekday {{ status }}" href="{{ url }}#{{ weekday.short_name }}{{ url_suffix }}">{{ name }}</a>
        % end
    % end
</div>
