
% from models.weekday import Weekday

% schedule_path = get('schedule_path')
% schedule_path_args = get('schedule_path_args', {})
% path_suffix = get('path_suffix', '')
% compact = get('compact', False)

<div class="weekdays {{ 'compact' if compact else '' }}">
    % for weekday in Weekday:
        % name = weekday.abbreviation if compact else weekday.short_name
        % if schedule:
            % status = schedule.get_weekday_status(weekday)
        % else:
            % status = ''
        % end
        % if schedule_path and schedule and weekday in schedule.weekdays:
            <a class="weekday {{ status }}" href="{{ context.url(schedule_path, f'#{weekday.short_name}{path_suffix}', **schedule_path_args) }}">{{ name }}</a>
        % else:
            <span class="weekday {{ status }}">{{ name }}</span>
        % end
    % end
</div>
