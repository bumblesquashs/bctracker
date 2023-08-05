
% from models.weekday import Weekday

% schedule_path = get('schedule_path')
% compact = get('compact', False)

<div class="weekdays {{ 'compact' if compact else '' }}">
    % for weekday in Weekday:
        % name = weekday.abbreviation if compact else weekday.short_name
        % if schedule is None:
            % status = 'no-service'
        % else:
            % status = schedule.get_weekday_status(weekday)
        % end
        % if schedule_path is None or schedule is None or weekday not in schedule.weekdays:
            <span class="weekday {{ status }}">{{ name }}</span>
        % else:
            <a class="weekday {{ status }}" href="{{ get_url(system, schedule_path + '#' + weekday.short_name, format='sheet', date=date) }}">{{ name }}</a>
        % end
    % end
</div>
