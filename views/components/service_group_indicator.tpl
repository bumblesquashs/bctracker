% import formatting

% schedule = service_group.schedule

<div class="service-indicator">
    % if get('compact', False):
        <div class="dates compact">
            <span class="date {{ 'running' if schedule.mon else '' }}">M</span>
            <span class="date {{ 'running' if schedule.tue else '' }}">T</span>
            <span class="date {{ 'running' if schedule.wed else '' }}">W</span>
            <span class="date {{ 'running' if schedule.thu else '' }}">T</span>
            <span class="date {{ 'running' if schedule.fri else '' }}">F</span>
            <span class="date {{ 'running' if schedule.sat else '' }}">S</span>
            <span class="date {{ 'running' if schedule.sun else '' }}">S</span>
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
                <span class="date {{ 'running' if schedule.mon else '' }}">Mon</span>
                <span class="date {{ 'running' if schedule.tue else '' }}">Tue</span>
                <span class="date {{ 'running' if schedule.wed else '' }}">Wed</span>
                <span class="date {{ 'running' if schedule.thu else '' }}">Thu</span>
                <span class="date {{ 'running' if schedule.fri else '' }}">Fri</span>
                <span class="date {{ 'running' if schedule.sat else '' }}">Sat</span>
                <span class="date {{ 'running' if schedule.sun else '' }}">Sun</span>
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
