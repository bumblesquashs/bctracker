
<div class="service-indicator">
    % schedule = service_group.schedule
    % if get('compact', False):
        <div class="dates compact">
            <span class="date {{ schedule.mon_status }}">M</span>
            <span class="date {{ schedule.tue_status }}">T</span>
            <span class="date {{ schedule.wed_status }}">W</span>
            <span class="date {{ schedule.thu_status }}">T</span>
            <span class="date {{ schedule.fri_status }}">F</span>
            <span class="date {{ schedule.sat_status }}">S</span>
            <span class="date {{ schedule.sun_status }}">S</span>
        </div>
    % else:
        % if schedule.special:
            <div class="title">Special Service</div>
            % if len(schedule.included_dates) > 0:
                <div class="details">{{ schedule.included_dates_string }}</div>
            % end
        % else:
            <div class="title">{{ service_group.date_string }}</div>
            <div class="dates">
                <span class="date {{ schedule.mon_status }}">Mon</span>
                <span class="date {{ schedule.tue_status }}">Tue</span>
                <span class="date {{ schedule.wed_status }}">Wed</span>
                <span class="date {{ schedule.thu_status }}">Thu</span>
                <span class="date {{ schedule.fri_status }}">Fri</span>
                <span class="date {{ schedule.sat_status }}">Sat</span>
                <span class="date {{ schedule.sun_status }}">Sun</span>
            </div>
            % if len(schedule.included_dates) > 0:
                <div class="details">Special Service: {{ schedule.included_dates_string }}</div>
            % end
            % if len(schedule.excluded_dates) > 0:
                <div class="details">No Service: {{ schedule.excluded_dates_string }}</div>
            % end
        % end
    % end
</div>
