<div class="service-indicator">
  <div class="service-indicator-section">
    <div class="service-indicator-day">Mon</div>
    % if len([s for s in services if s.mon]) > 0:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Tue</div>
    % if len([s for s in services if s.tue]) > 0:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Wed</div>
    % if len([s for s in services if s.wed]) > 0:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Thu</div>
    % if len([s for s in services if s.thu]) > 0:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Fri</div>
    % if len([s for s in services if s.fri]) > 0:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Sat</div>
    % if len([s for s in services if s.sat]) > 0:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
  <div class="service-indicator-section">
    <div class="service-indicator-day">Sun</div>
    % if len([s for s in services if s.sun]) > 0:
      <img class="service-indicator-check" src="/img/check.png" />
    % end
  </div>
</div>
  