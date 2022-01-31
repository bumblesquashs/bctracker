% if adherence is not None:
    <span class="tooltip-anchor adherence-indicator {{ adherence.status_class }}">
        {{ adherence }}
        <div class="tooltip">{{ adherence.description }}</div>
    </span>
% end
