
% if adherence is not None:
    <div class="tooltip-anchor adherence {{ adherence.status_class }} {{ get('size', '') }}">
        {{ adherence }}
        <div class="tooltip">{{ adherence.description }}</div>
    </div>
% end
