<div class="service-indicator">
    % if pattern is None:
        <div class="title">No Service</div>
    % elif get('compact', False):
        <div class="dates compact">
            <span class="date {{ pattern.mon_status }}">M</span>
            <span class="date {{ pattern.tue_status }}">T</span>
            <span class="date {{ pattern.wed_status }}">W</span>
            <span class="date {{ pattern.thu_status }}">T</span>
            <span class="date {{ pattern.fri_status }}">F</span>
            <span class="date {{ pattern.sat_status }}">S</span>
            <span class="date {{ pattern.sun_status }}">S</span>
        </div>
    % else:
        % if pattern.special:
            <div class="title">Special Service</div>
            <div class="details">{{ pattern.date_string }}</div>
        % else:
            <div class="title">{{ pattern.date_string }}</div>
            <div class="dates">
                <span class="date {{ pattern.mon_status }}">Mon</span>
                <span class="date {{ pattern.tue_status }}">Tue</span>
                <span class="date {{ pattern.wed_status }}">Wed</span>
                <span class="date {{ pattern.thu_status }}">Thu</span>
                <span class="date {{ pattern.fri_status }}">Fri</span>
                <span class="date {{ pattern.sat_status }}">Sat</span>
                <span class="date {{ pattern.sun_status }}">Sun</span>
            </div>
            % if len(pattern.included_dates) > 0:
                <div class="details">Special Service: {{ pattern.included_dates_string }}</div>
            % end
            % if len(pattern.excluded_dates) > 0:
                <div class="details">No Service: {{ pattern.excluded_dates_string }}</div>
            % end
        % end
    % end
</div>
