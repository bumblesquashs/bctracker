
% from datetime import timedelta

% from models.date import Date
% from models.time import Time

% service_group = get('service_group')
% date = get('date')

% current_trip = get('trip')

% start_time = block.get_start_time(service_group=service_group, date=date)
% end_time = block.get_end_time(service_group=service_group, date=date)
% total_minutes = end_time.get_minutes() - start_time.get_minutes()

% if total_minutes > 0:
    <div class="block-timeline">
        <div class="row space-between smaller-font lighter-text">
            <div>{{ start_time.format_web(time_format) }}</div>
            <div>{{ end_time.format_web(time_format) }}</div>
        </div>
        <div class="timeline">
            % for trip in block.get_trips(service_group=service_group, date=date):
                % trip_minutes = trip.end_time.get_minutes() - trip.start_time.get_minutes()
                % percentage = (trip_minutes / total_minutes) * 100
                % offset_minutes = trip.start_time.get_minutes() - start_time.get_minutes()
                % offset_percentage = (offset_minutes / total_minutes) * 100
                <a href="{{ get_url(trip.context, 'trips', trip) }}" class="section tooltip-anchor {{ 'non-current' if current_trip and trip != current_trip else '' }}" style="background-color: #{{ trip.route.colour }}; width: {{ percentage }}%; left: {{ offset_percentage }}%;">
                    <div class="tooltip right">
                        <div class="title">{{ trip }}</div>
                        {{ trip.start_time.format_web(time_format) }} - {{ trip.end_time.format_web(time_format) }}
                    </div>
                </a>
            % end
            
            % date = Date.today(block.context.timezone)
            % time = Time.now(block.context.timezone)
            % if start_time < time and end_time > time and date in block.schedule:
                % offset_minutes = time.get_minutes() - start_time.get_minutes()
                % offset_percentage = (offset_minutes / total_minutes) * 100
                <div class="now" style="left: {{ offset_percentage }}%;">
                    
                </div>
            % end
        </div>
        <div class="timespan">
            % clock_time = Time(start_time.hour, 0, None, start_time.timezone)
            % while clock_time <= end_time:
                % if clock_time >= start_time:
                    % offset_minutes = clock_time.get_minutes() - start_time.get_minutes()
                    % offset_percentage = (offset_minutes / total_minutes) * 100
                    <div class="time {{ 'hour' if clock_time.minute == 0 else '' }}" style="left: {{ offset_percentage }}%;">
                        
                    </div>
                % end
                % clock_time += timedelta(minutes=15)
            % end
        </div>
    </div>
% end
