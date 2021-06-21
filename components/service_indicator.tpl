<div class="service-indicator">
  <div class="service-indicator-section">
    <div class="service-indicator-day">Mon</div>
    % mon = False
    % if defined('service'):
      % mon = service.mon
    % elif defined('services'):
      % mon = len([s for s in services if s.mon]) > 0
    % end
    % if mon:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Tue</div>
    % tue = False
    % if defined('service'):
      % tue = service.tue
    % elif defined('services'):
      % tue = len([s for s in services if s.tue]) > 0
    % end
    % if tue:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Wed</div>
    % wed = False
    % if defined('service'):
      % wed = service.wed
    % elif defined('services'):
      % wed = len([s for s in services if s.wed]) > 0
    % end
    % if wed:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Thu</div>
    % thu = False
    % if defined('service'):
      % thu = service.thu
    % elif defined('services'):
      % thu = len([s for s in services if s.thu]) > 0
    % end
    % if thu:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Fri</div>
    % fri = False
    % if defined('service'):
      % fri = service.fri
    % elif defined('services'):
      % fri = len([s for s in services if s.fri]) > 0
    % end
    % if fri:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Sat</div>
    % sat = False
    % if defined('service'):
      % sat = service.sat
    % elif defined('services'):
      % sat = len([s for s in services if s.sat]) > 0
    % end
    % if sat:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Sun</div>
    % sun = False
    % if defined('service'):
      % sun = service.sun
    % elif defined('services'):
      % sun = len([s for s in services if s.sun]) > 0
    % end
    % if sun:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  % if defined('service') and len(service.special_dates) > 0:
    <div class="service-details">{{ service.special_dates_string }}</div>
  % end
</div>
