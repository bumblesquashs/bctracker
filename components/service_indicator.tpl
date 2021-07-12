% from models.service import ServiceType

<div class="service-indicator">
  <div class="service-indicator-header">{{ service.date_string }}</div>
  % if service.type == ServiceType.SPECIAL:
    % if len(service.special_dates) > 0:
      <div class="service-details">{{ service.special_dates_string }}</div>
    % end
  % else:
    <div class="service-indicator-section">
      <div class="service-indicator-day">Mon</div>
      % if service.mon:
        <img class="service-indicator-check" src="/img/check.png" />
      % end
    </div>
    <div class="service-indicator-section">
      <div class="service-indicator-day">Tue</div>
      % if service.tue:
        <img class="service-indicator-check" src="/img/check.png" />
      % end
    </div>
    <div class="service-indicator-section">
      <div class="service-indicator-day">Wed</div>
      % if service.wed:
        <img class="service-indicator-check" src="/img/check.png" />
      % end
    </div>
    <div class="service-indicator-section">
      <div class="service-indicator-day">Thu</div>
      % if service.thu:
        <img class="service-indicator-check" src="/img/check.png" />
      % end
    </div>
    <div class="service-indicator-section">
      <div class="service-indicator-day">Fri</div>
      % if service.fri:
        <img class="service-indicator-check" src="/img/check.png" />
      % end
    </div>
    <div class="service-indicator-section">
      <div class="service-indicator-day">Sat</div>
      % if service.sat:
        <img class="service-indicator-check" src="/img/check.png" />
      % end
    </div>
    <div class="service-indicator-section">
      <div class="service-indicator-day">Sun</div>
      % if service.sun:
        <img class="service-indicator-check" src="/img/check.png" />
      % end
    </div>
    % if len(service.special_dates) > 0:
      <div class="service-details">Special Service: {{ service.special_dates_string }}</div>
    % end
  % end
</div>
