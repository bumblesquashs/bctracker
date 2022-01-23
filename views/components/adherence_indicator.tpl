% if adherence is not None:
    <span class="tooltip-anchor adherence-indicator {{ adherence.status }}">
        {{ adherence }}
        <div class="tooltip">{{ adherence.description }}</div>
    </span>
% end
