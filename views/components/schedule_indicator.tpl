
% from models.weekday import Weekday

<div class="service-indicator">
    % if schedule is None:
        <div class="title">No Service</div>
    % elif get('compact', False):
        <div class="dates compact">
            <span class="date {{ schedule.get_status(Weekday.MON) }}">M</span>
            <span class="date {{ schedule.get_status(Weekday.TUE) }}">T</span>
            <span class="date {{ schedule.get_status(Weekday.WED) }}">W</span>
            <span class="date {{ schedule.get_status(Weekday.THU) }}">T</span>
            <span class="date {{ schedule.get_status(Weekday.FRI) }}">F</span>
            <span class="date {{ schedule.get_status(Weekday.SAT) }}">S</span>
            <span class="date {{ schedule.get_status(Weekday.SUN) }}">S</span>
        </div>
    % else:
        % if schedule.special:
            <div class="title">Special Service</div>
            <div class="details">{{ schedule.date_string }}</div>
        % else:
            <div class="title">{{ schedule.date_string }}</div>
            <div class="dates">
                <span class="date {{ schedule.get_status(Weekday.MON) }}">Mon</span>
                <span class="date {{ schedule.get_status(Weekday.TUE) }}">Tue</span>
                <span class="date {{ schedule.get_status(Weekday.WED) }}">Wed</span>
                <span class="date {{ schedule.get_status(Weekday.THU) }}">Thu</span>
                <span class="date {{ schedule.get_status(Weekday.FRI) }}">Fri</span>
                <span class="date {{ schedule.get_status(Weekday.SAT) }}">Sat</span>
                <span class="date {{ schedule.get_status(Weekday.SUN) }}">Sun</span>
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
