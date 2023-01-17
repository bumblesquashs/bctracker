
% from models.date import Date
% from models.time import Time

% start_time = block.get_start_time()
% end_time = block.get_end_time()
% total_minutes = end_time.get_minutes() - start_time.get_minutes()

<div class="flex-row">
    <div class="smaller-font lighter-text">{{ start_time.format_web() }}</div>
    <div class="flex-1"></div>
    <div class="smaller-font lighter-text">{{ end_time.format_web() }}</div>
</div>
<div class="block-indicator">
    % for trip in block.get_trips():
        % trip_minutes = trip.end_time.get_minutes() - trip.start_time.get_minutes()
        % percentage = (trip_minutes / total_minutes) * 100
        % offset_minutes = trip.start_time.get_minutes() - start_time.get_minutes()
        % offset_percentage = (offset_minutes / total_minutes) * 100
        <div class="trip" style="background-color: #{{ trip.route.colour }}; width: {{ percentage }}%; left: {{ offset_percentage }}%;">
            
        </div>
    % end
    
    % if start_time.is_earlier and end_time.is_later and block.schedule.includes(Date.today()):
        % now = Time.now(block.system.timezone)
        % offset_minutes = now.get_minutes() - start_time.get_minutes()
        % offset_percentage = (offset_minutes / total_minutes) * 100
        <div class="now" style="left: {{ offset_percentage }}%;">
            
        </div>
    % end
</div>