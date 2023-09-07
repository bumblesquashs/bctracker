
% from models.weekday import Weekday

% schedule_path = get('schedule_path')
% path_suffix = get('path_suffix', '')
% compact = get('compact', False)

% if schedule is None:
    % service_weekdays = set()
% else:
    % service_weekdays = {d.weekday for d in schedule.date_range}
% end

<div class="weekdays {{ 'compact' if compact else '' }}">
    % for weekday in Weekday:
        % name = weekday.abbreviation if compact else weekday.short_name
        % if weekday in service_weekdays:
            % status = schedule.get_weekday_status(weekday)
        % else:
            % status = ''
        % end
        % if schedule_path is None or schedule is None or weekday not in schedule.weekdays:
            <span class="weekday {{ status }}">{{ name }}</span>
        % else:
            <a class="weekday {{ status }}" href="{{ get_url(system, f'{schedule_path}#{weekday.short_name}{path_suffix}') }}">{{ name }}</a>
        % end
    % end
</div>
