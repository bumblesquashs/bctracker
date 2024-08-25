
% if adherence:
    <div class="tooltip-anchor adherence-indicator {{ adherence.status_class }} {{ get('size', '') }}">
        {{ adherence }}
        <div class="tooltip right">{{ adherence.description }}</div>
    </div>
% end
