% import formatting

<div class="service-indicator">
    % if get('compact', False):
        <div class="dates compact">
            <span class="date {{ 'running' if len([s for s in services if s.mon]) > 0 else '' }}">M</span>
            <span class="date {{ 'running' if len([s for s in services if s.tue]) > 0 else '' }}">T</span>
            <span class="date {{ 'running' if len([s for s in services if s.wed]) > 0 else '' }}">W</span>
            <span class="date {{ 'running' if len([s for s in services if s.thu]) > 0 else '' }}">T</span>
            <span class="date {{ 'running' if len([s for s in services if s.fri]) > 0 else '' }}">F</span>
            <span class="date {{ 'running' if len([s for s in services if s.sat]) > 0 else '' }}">S</span>
            <span class="date {{ 'running' if len([s for s in services if s.sun]) > 0 else '' }}">S</span>
        </div>
    % else:
        % start_date = None
        % end_date = None
        % for service in services:
            % if start_date is None or service.start_date < start_date:
                % start_date = service.start_date
            % end
            % if end_date is None or service.end_date > end_date:
                % end_date = service.end_date
            % end
        % end
        % if start_date is None or end_date is None:
            <div class="title">Service Days</div>
        % else:
            <div class="title">{{ formatting.long(start_date) }} to {{ formatting.long(end_date) }}</div>
        % end
        <div class="dates">
            <span class="date {{ 'running' if len([s for s in services if s.mon]) > 0 else '' }}">Mon</span>
            <span class="date {{ 'running' if len([s for s in services if s.tue]) > 0 else '' }}">Tue</span>
            <span class="date {{ 'running' if len([s for s in services if s.wed]) > 0 else '' }}">Wed</span>
            <span class="date {{ 'running' if len([s for s in services if s.thu]) > 0 else '' }}">Thu</span>
            <span class="date {{ 'running' if len([s for s in services if s.fri]) > 0 else '' }}">Fri</span>
            <span class="date {{ 'running' if len([s for s in services if s.sat]) > 0 else '' }}">Sat</span>
            <span class="date {{ 'running' if len([s for s in services if s.sun]) > 0 else '' }}">Sun</span>
        </div>
    % end
</div>
