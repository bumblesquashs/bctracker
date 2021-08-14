% from models.service import ServiceType

<div class="service-indicator">
    <div class="title">{{ service.date_string }}</div>
    % if service.type == ServiceType.SPECIAL:
        % if len(service.special_dates) > 0:
            <div class="details">{{ service.special_dates_string }}</div>
        % end
    % else:
        <div class="date">
            <div class="name">Mon</div>
            % if service.mon:
                <img class="light-only check" src="/img/check.png" />
                <img class="dark-only check" src="/img/check-white.png" />
            % end
        </div>
        <div class="date">
            <div class="name">Tue</div>
            % if service.tue:
                <img class="light-only check" src="/img/check.png" />
                <img class="dark-only check" src="/img/check-white.png" />
            % end
        </div>
        <div class="date">
            <div class="day">Wed</div>
            % if service.wed:
                <img class="light-only check" src="/img/check.png" />
                <img class="dark-only check" src="/img/check-white.png" />
            % end
        </div>
        <div class="date">
            <div class="name">Thu</div>
            % if service.thu:
                <img class="light-only check" src="/img/check.png" />
                <img class="dark-only check" src="/img/check-white.png" />
            % end
        </div>
        <div class="date">
            <div class="name">Fri</div>
            % if service.fri:
                <img class="light-only check" src="/img/check.png" />
                <img class="dark-only check" src="/img/check-white.png" />
            % end
        </div>
        <div class="date">
            <div class="name">Sat</div>
            % if service.sat:
                <img class="light-only check" src="/img/check.png" />
                <img class="dark-only check" src="/img/check-white.png" />
            % end
        </div>
        <div class="date">
            <div class="name">Sun</div>
            % if service.sun:
                <img class="light-only check" src="/img/check.png" />
                <img class="dark-only check" src="/img/check-white.png" />
            % end
        </div>
        % if len(service.special_dates) > 0:
            <div class="details">Special Service: {{ service.special_dates_string }}</div>
        % end
    % end
</div>
