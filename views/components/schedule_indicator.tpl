
% import calendar
% from models.weekday import Weekday

% url = get('url', None)
% date_url = get('date_url', url)
% url_suffix = get('url_suffix', '')

<div class="schedule {{ 'special' if schedule.special else 'normal' }}">
    % if get('compact', False):
        <div class="weekdays compact">
            % for weekday in Weekday:
                % status = schedule.get_weekday_status(weekday)
                % if url is None or weekday not in schedule.weekdays:
                    <span class="weekday {{ status }}">{{ weekday.abbreviation }}</span>
                % else:
                    <a class="weekday {{ status }}" href="{{ url }}#{{ weekday.short_name }}{{ url_suffix }}">{{ weekday.abbreviation }}</a>
                % end
            % end
        </div>
    % else:
        <div class="title">{{ schedule.date_string }}</div>
        <div class="legend">
            <div>
                <span class="icon normal-service"></span> Normal Service
            </div>
            % if not schedule.special:
                % if len(schedule.modified_dates) > 0:
                    <div>
                        <span class="icon modified-service"></span> Modified Service
                    </div>
                % end
                % if len(schedule.excluded_dates) > 0 or len(schedule.weekdays) < 7:
                    <div>
                        <span class="icon no-service"></span> No Service
                    </div>
                % end
            % end
        </div>
        
        % if not schedule.special:
            <div class="weekdays">
                % for weekday in Weekday:
                    % status = schedule.get_weekday_status(weekday)
                    % if url is None or weekday not in schedule.weekdays:
                        <span class="weekday {{ status }}">{{ weekday.short_name }}</span>
                    % else:
                        <a class="weekday {{ status }}" href="{{ url }}#{{ weekday.short_name }}{{ url_suffix }}">{{ weekday.short_name }}</a>
                    % end
                % end
            </div>
        % end
        
        % dates = schedule.modified_dates.union(schedule.excluded_dates)
        % if len(dates) > 0:
            <div class="exceptions">
                <div class="months">
                    % for (year, month) in sorted({(d.year, d.month) for d in dates}):
                        % month_dates = sorted({d for d in dates if d.month == month and d.year == year})
                        <div class="month">
                            <div class="name">{{ calendar.month_name[month] }}</div>
                            % for date in month_dates:
                                % status = schedule.get_date_status(date)
                                % if date_url is None or date in schedule.excluded_dates:
                                    <span class="date {{ status }}">{{ date.day }}</span>
                                % else:
                                    <a class="date {{ status }}" href="{{ date_url }}/{{ date.format_db() }}">{{ date.day }}</a>
                                % end
                            % end
                        </div>
                    % end
                </div>
            </div>
        % end
    % end
</div>
