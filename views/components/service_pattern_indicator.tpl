% from models.date import Weekday
% from models.service import ServiceGroup

<div class="service-indicator">
    % if pattern is None:
        <div class="title">No Service</div>
    % elif get('compact', False):
        <div class="dates compact">
            <span class="date {{ pattern.get_status(Weekday.MON) }}">M</span>
            <span class="date {{ pattern.get_status(Weekday.TUE) }}">T</span>
            <span class="date {{ pattern.get_status(Weekday.WED) }}">W</span>
            <span class="date {{ pattern.get_status(Weekday.THU) }}">T</span>
            <span class="date {{ pattern.get_status(Weekday.FRI) }}">F</span>
            <span class="date {{ pattern.get_status(Weekday.SAT) }}">S</span>
            <span class="date {{ pattern.get_status(Weekday.SUN) }}">S</span>
        </div>
    % else:
        % if pattern.special:
            <div class="title">Special Service</div>
            <div class="details">{{ pattern.date_string }}</div>
        % else:
            <div class="title">{{ pattern.date_string }}</div>
            <div class="dates">
                <span class="date {{ pattern.get_status(Weekday.MON) }}">Mon</span>
                <span class="date {{ pattern.get_status(Weekday.TUE) }}">Tue</span>
                <span class="date {{ pattern.get_status(Weekday.WED) }}">Wed</span>
                <span class="date {{ pattern.get_status(Weekday.THU) }}">Thu</span>
                <span class="date {{ pattern.get_status(Weekday.FRI) }}">Fri</span>
                <span class="date {{ pattern.get_status(Weekday.SAT) }}">Sat</span>
                <span class="date {{ pattern.get_status(Weekday.SUN) }}">Sun</span>
            </div>
            % if len(pattern.included_dates) > 0:
                <div class="details">Special Service: {{ pattern.included_dates_string }}</div>
            % end
            % if len(pattern.excluded_dates) > 0:
                <div class="details">No Service: {{ pattern.excluded_dates_string }}</div>
            % end
            % if type(pattern) is ServiceGroup and len(pattern.modified_dates) > 0:
                <div class="details">Modified Service: {{ pattern.modified_dates_string }}</div>
            % end
        % end
    % end
</div>
