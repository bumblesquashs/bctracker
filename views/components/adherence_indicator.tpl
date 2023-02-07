
% if adherence is not None:
    <div class="tooltip-anchor adherence-indicator {{ adherence.status_class }} {{ get('size', '') }}">
        {{ adherence }}
        <div class="tooltip">
            <div class="title">{{ adherence.description }}</div>
        </div>
    </div>
% end
