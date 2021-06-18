<table class="service-indicator">
  <thead>
    <tr>
      <th>Mon</th>
      <th>Tue</th>
      <th>Wed</th>
      <th>Thu</th>
      <th>Fri</th>
      <th>Sat</th>
      <th>Sun</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        % mon = False
        % if defined('service'):
          % mon = service.mon
        % elif defined('services'):
          % mon = len([s for s in services if s.mon]) > 0
        % end
        % if mon:
          <img class="service-check" src="/img/check.png" />
        % end
      </td>
      <td>
        % tue = False
        % if defined('service'):
          % tue = service.tue
        % elif defined('services'):
          % tue = len([s for s in services if s.tue]) > 0
        % end
        % if tue:
          <img class="service-check" src="/img/check.png" />
        % end
      </td>
      <td>
        % wed = False
        % if defined('service'):
          % wed = service.wed
        % elif defined('services'):
          % wed = len([s for s in services if s.wed]) > 0
        % end
        % if wed:
          <img class="service-check" src="/img/check.png" />
        % end
      </td>
      <td>
        % thu = False
        % if defined('service'):
          % thu = service.thu
        % elif defined('services'):
          % thu = len([s for s in services if s.thu]) > 0
        % end
        % if thu:
          <img class="service-check" src="/img/check.png" />
        % end
      </td>
      <td>
        % fri = False
        % if defined('service'):
          % fri = service.fri
        % elif defined('services'):
          % fri = len([s for s in services if s.fri]) > 0
        % end
        % if fri:
          <img class="service-check" src="/img/check.png" />
        % end
      </td>
      <td>
        % sat = False
        % if defined('service'):
          % sat = service.sat
        % elif defined('services'):
          % sat = len([s for s in services if s.sat]) > 0
        % end
        % if sat:
          <img class="service-check" src="/img/check.png" />
        % end
      </td>
      <td>
        % sun = False
        % if defined('service'):
          % sun = service.sun
        % elif defined('services'):
          % sun = len([s for s in services if s.sun]) > 0
        % end
        % if sun:
          <img class="service-check" src="/img/check.png" />
        % end
      </td>
    </tr>
  </tbody>
</table>

% if defined('service') and len(service.special_dates) > 0:
  <div class="service-details">{{ service.special_dates_string }} Only</div>
% end
