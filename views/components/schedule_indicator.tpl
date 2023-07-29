
% import calendar

% url = get('url', None)
% date_url = get('date_url', url)

<div class="schedule-indicator">
    <div class="legend">
        <div class="flex-row flex-gap-5">
            <div class="icon normal-service"></div>
            <div>Normal Service</div>
        </div>
        <div class="flex-row flex-gap-5">
            <div class="icon modified-service"></div>
            <div>Modified Service</div>
        </div>
        <div class="flex-row flex-gap-5">
            <div class="icon no-service"></div>
            <div>No Service</div>
        </div>
    </div>
    <div class="schedule">
        % include('components/weekdays_indicator', schedule=schedule)
        % dates = schedule.exceptions.union(schedule.modifications)
        % if len(dates) > 0:
            <div class="exceptions">
                % for (year, month) in sorted({(d.year, d.month) for d in dates}):
                    % month_dates = sorted({d for d in dates if d.month == month and d.year == year})
                    <div class="month">
                        <div class="name">{{ calendar.month_name[month] }}</div>
                        % for date in month_dates:
                            % status = schedule.get_date_status(date)
                            % if date_url is None:
                                <span class="date {{ status }}">{{ date.day }}</span>
                            % else:
                                <a class="date {{ status }}" href="{{ date_url }}/{{ date.format_db() }}">{{ date.day }}</a>
                            % end
                        % end
                    </div>
                % end
            </div>
        % end
    </div>
    % if url is not None:
        <div class="footer">
            Click on a weekday or date to jump to the schedule for that day
        </div>
    % end
</div>
