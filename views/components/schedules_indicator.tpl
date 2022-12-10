
% import calendar

% url = get('url', None)
% date_url = get('date_url', url)

% show_special_schedules = len([s for s in schedules if not s.special]) == 0
% modified_dates = {d for s in schedules for d in s.modified_dates}
% excluded_dates = {d for s in schedules for d in s.excluded_dates}

<div class="schedules">
    <div class="legend">
        % if len([s for s in schedules if not s.special]) > 0:
            <div>
                <span class="icon normal-service"></span> Normal Service
            </div>
        % end
        % if len(modified_dates) > 0:
            <div>
                <span class="icon modified-service"></span> Modified Service
            </div>
        % end
        % if len(excluded_dates) > 0 or len([s for s in schedules if len(s.weekdays) < 7]) > 0 or show_special_schedules:
            <div>
                <span class="icon no-service"></span> No Service
            </div>
        % end
    </div>
    % for (i, schedule) in enumerate(schedules):
        % if not schedule.special or show_special_schedules:
            <div class="schedule">
                <div class="title">{{ schedule.date_string }}</div>
                % include('components/weekdays_indicator', schedule=schedule, url_suffix='' if i == 0 else f'{i + 1}')
            </div>
        % end
    % end
    % dates = modified_dates.union(excluded_dates)
    % if len(dates) > 0:
        <div class="exceptions">
            % for (year, month) in sorted({(d.year, d.month) for d in dates}):
                % month_dates = sorted({d for d in dates if d.month == month and d.year == year})
                <div class="month">
                    <div class="name">{{ calendar.month_name[month] }}</div>
                    % for date in month_dates:
                        % if date in modified_dates:
                            % status = 'modified-service'
                        % elif date in excluded_dates:
                            % status = 'no-service'
                        % else:
                            % status = 'normal-service'
                        % end
                        % if date_url is None or date in schedule.excluded_dates:
                            <span class="date {{ status }}">{{ date.day }}</span>
                        % else:
                            <a class="date {{ status }}" href="{{ date_url }}/{{ date.format_db() }}">{{ date.day }}</a>
                        % end
                    % end
                </div>
            % end
        </div>
    % end
    % if url is not None:
        <div class="footer">
            Click on a weekday or date to jump to the schedule for that day
        </div>
    % end
</div>
