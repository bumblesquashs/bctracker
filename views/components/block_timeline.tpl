
% from models.time import Time

% service_group = get('service_group')
% date = get('date')

% start_time = block.get_start_time(service_group=service_group, date=date)
% end_time = block.get_end_time(service_group=service_group, date=date)
% total_minutes = end_time.get_minutes() - start_time.get_minutes()

<div class="column">
    <div class="row">
        <div class="smaller-font lighter-text">{{ start_time.format_web(time_format) }}</div>
        <div class="flex-1"></div>
        <div class="smaller-font lighter-text">{{ end_time.format_web(time_format) }}</div>
    </div>
    <div class="block-indicator">
        % for trip in block.get_trips(service_group=service_group, date=date):
            % trip_minutes = trip.end_time.get_minutes() - trip.start_time.get_minutes()
            % percentage = (trip_minutes / total_minutes) * 100
            % offset_minutes = trip.start_time.get_minutes() - start_time.get_minutes()
            % offset_percentage = (offset_minutes / total_minutes) * 100
            <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}" class="trip tooltip-anchor" style="background-color: #{{ trip.route.colour }}; width: {{ percentage }}%; left: {{ offset_percentage }}%;">
                <div class="tooltip">
                    <div class="title">{{ trip }}</div>
                    {{ trip.start_time.format_web(time_format) }} - {{ trip.end_time.format_web(time_format) }}
                </div>
            </a>
        % end
        
        % if start_time.is_earlier and end_time.is_later and block.schedule.is_today:
            % time = Time.now(block.system.timezone)
            % offset_minutes = time.get_minutes() - start_time.get_minutes()
            % offset_percentage = (offset_minutes / total_minutes) * 100
            <div class="now" style="left: {{ offset_percentage }}%;">
                
            </div>
        % end
    </div>
</div>
