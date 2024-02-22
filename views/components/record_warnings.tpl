% if len(record.warnings) > 0:
    <div class="tooltip-anchor record-warnings">
        <img class="white inline" src="/img/white/warning.png" />
        <img class="black inline" src="/img/black/warning.png" />
        <div class="tooltip">
            <div class="title">Potential accidental login</div>
            % for warning in record.warnings:
                <div>{{ warning }}</div>
            % end
        </div>
    </div>
% end
