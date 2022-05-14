
% if adherence is not None:
    <span class="tooltip-anchor adherence-indicator {{ adherence.status_class }} {{ get('size', '') }}">
        {{ adherence }}
        <div class="tooltip">{{ adherence.description }}</div>
    </span>
% end
