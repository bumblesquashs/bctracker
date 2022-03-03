<div class="service-indicator">
    % if get('compact', False):
        <div class="dates compact">
            <span class="date {{ 'running' if service.mon else '' }}">M</span>
            <span class="date {{ 'running' if service.tue else '' }}">T</span>
            <span class="date {{ 'running' if service.wed else '' }}">W</span>
            <span class="date {{ 'running' if service.thu else '' }}">T</span>
            <span class="date {{ 'running' if service.fri else '' }}">F</span>
            <span class="date {{ 'running' if service.sat else '' }}">S</span>
            <span class="date {{ 'running' if service.sun else '' }}">S</span>
        </div>
    % else:
        % if service.special:
            <div class="title">Special Service</div>
            % if len(service.included_dates) > 0:
                <div class="details">{{ service.included_dates_string }}</div>
            % end
        % else:
            <div class="title">{{ service.date_string }}</div>
            <div class="dates">
                <span class="date {{ 'running' if service.mon else '' }}">Mon</span>
                <span class="date {{ 'running' if service.tue else '' }}">Tue</span>
                <span class="date {{ 'running' if service.wed else '' }}">Wed</span>
                <span class="date {{ 'running' if service.thu else '' }}">Thu</span>
                <span class="date {{ 'running' if service.fri else '' }}">Fri</span>
                <span class="date {{ 'running' if service.sat else '' }}">Sat</span>
                <span class="date {{ 'running' if service.sun else '' }}">Sun</span>
            </div>
            % if len(service.included_dates) > 0:
                <div class="details">Special Service: {{ service.included_dates_string }}</div>
            % end
            % if len(service.excluded_dates) > 0:
                <div class="details">No Service: {{ service.excluded_dates_string }}</div>
            % end
        % end
    % end
</div>
