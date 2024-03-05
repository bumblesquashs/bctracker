
% from models.weekday import Weekday

% schedule_path = get('schedule_path')
% path_suffix = get('path_suffix', '')
% compact = get('compact', False)

<div class="weekdays {{ 'compact' if compact else '' }}">
    % for weekday in Weekday:
        % name = weekday.abbreviation if compact else weekday.short_name
        % if schedule is None:
            % status = ''
        % else:
            % status = schedule.get_weekday_status(weekday)
        % end
        % if schedule_path is None or schedule is None or weekday not in schedule.weekdays:
            <span class="weekday {{ status }}">{{ name }}</span>
        % else:
            <a class="weekday {{ status }}" href="{{ get_url(system, agency, f'/{schedule_path}#{weekday.short_name}{path_suffix}') }}">{{ name }}</a>
        % end
    % end
</div>
