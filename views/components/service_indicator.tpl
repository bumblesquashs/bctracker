% from models.service import ServiceType

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
        <div class="title">{{ service.date_string }}</div>
        % if service.type == ServiceType.SPECIAL:
            % if len(service.special_dates) > 0:
                <div class="details">{{ service.special_dates_string }}</div>
            % end
        % else:
            <div class="dates">
                <span class="date {{ 'running' if service.mon else '' }}">Mon</span>
                <span class="date {{ 'running' if service.tue else '' }}">Tue</span>
                <span class="date {{ 'running' if service.wed else '' }}">Wed</span>
                <span class="date {{ 'running' if service.thu else '' }}">Thu</span>
                <span class="date {{ 'running' if service.fri else '' }}">Fri</span>
                <span class="date {{ 'running' if service.sat else '' }}">Sat</span>
                <span class="date {{ 'running' if service.sun else '' }}">Sun</span>
            </div>
            % if len(service.special_dates) > 0:
                <div class="details">Special Service: {{ service.special_dates_string }}</div>
            % end
        % end
    % end
</div>
