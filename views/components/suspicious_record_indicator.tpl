% if record.is_suspicious:
    % minutes = record.total_seen_minutes
    <div class="tooltip-anchor">
        <img class="middle-align white inline" src="/img/white/warning.png" />
        <img class="middle-align black inline" src="/img/black/warning.png" />
        <div class="tooltip">
            <div class="title">Potential accidental login</div>
            Bus was logged in for only {{ minutes }} {{ 'minute' if minutes == 1 else 'minutes' }}
        </div>
    </div>
% end
