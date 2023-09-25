
% import calendar

% schedule_path = get('schedule_path')
% date_path = get('date_path', schedule_path)

% has_normal_service = any(s.has_normal_service for s in schedules)
% has_modified_service = any(s.has_modified_service for s in schedules)
% has_no_service = any(s.has_no_service for s in schedules)

<div class="schedules-indicator">
    % if has_normal_service or has_modified_service or has_no_service:
        <div class="legend">
            % if has_normal_service:
                <div class="flex-row flex-gap-5">
                    <div class="icon normal-service"></div>
                    <div>Normal Service</div>
                </div>
            % end
            % if has_modified_service:
                <div class="flex-row flex-gap-5">
                    <div class="icon modified-service"></div>
                    <div>Modified Service</div>
                </div>
            % end
            % if has_no_service:
                <div class="flex-row flex-gap-5">
                    <div class="icon no-service"></div>
                    <div>No Service</div>
                </div>
            % end
        </div>
    % end
    <div class="flex-column flex-gap-10">
        % for (i, schedule) in enumerate(schedules):
            <div class="schedule">
                % if not schedule.is_special:
                    <div class="title">{{ schedule.date_range }}</div>
                    % include('components/weekdays_indicator', schedule=schedule, path_suffix='' if i == 0 else str(i + 1))
                % end
                % dates = schedule.all_dates
                % if len(dates) > 0:
                    <div class="exceptions">
                        % for (year, month) in sorted({(d.year, d.month) for d in dates}):
                            % month_dates = sorted({d for d in dates if d.month == month and d.year == year})
                            <div class="month {{ 'title' if schedule.is_special else '' }}">
                                <div class="name">{{ calendar.month_name[month] }}</div>
                                % for date in month_dates:
                                    % status = schedule.get_date_status(date)
                                    % if schedule_path is None:
                                        <span class="date {{ status }}">{{ date.day }}</span>
                                    % else:
                                        <a class="date {{ status }}" href="{{ get_url(system, f'{date_path}/{date.format_db()}') }}">{{ date.day }}</a>
                                    % end
                                % end
                            </div>
                        % end
                    </div>
                % end
            </div>
        % end
    </div>
    % if schedule_path is not None:
        <div class="footer">
            Click on a weekday or date to jump to the schedule for that day
        </div>
    % end
</div>
