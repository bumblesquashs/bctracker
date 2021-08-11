<div class="service-indicator">
    <div class="date">
        <div class="name">Mon</div>
        % if len([s for s in services if s.mon]) > 0:
            <img class="check" src="/img/check.png" />
        % end
    </div>
    <div class="date">
        <div class="name">Tue</div>
        % if len([s for s in services if s.tue]) > 0:
            <img class="check" src="/img/check.png" />
        % end
    </div>
    <div class="date">
        <div class="name">Wed</div>
        % if len([s for s in services if s.wed]) > 0:
            <img class="check" src="/img/check.png" />
        % end
    </div>
    <div class="date">
        <div class="name">Thu</div>
        % if len([s for s in services if s.thu]) > 0:
            <img class="check" src="/img/check.png" />
        % end
    </div>
    <div class="date">
        <div class="name">Fri</div>
        % if len([s for s in services if s.fri]) > 0:
            <img class="check" src="/img/check.png" />
        % end
    </div>
    <div class="date">
        <div class="name">Sat</div>
        % if len([s for s in services if s.sat]) > 0:
            <img class="check" src="/img/check.png" />
        % end
    </div>
    <div class="date">
        <div class="name">Sun</div>
        % if len([s for s in services if s.sun]) > 0:
            <img class="check" src="/img/check.png" />
        % end
    </div>
</div>
  