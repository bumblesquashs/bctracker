
% if adherence:
    <div class="tooltip-anchor adherence-indicator {{ adherence.status_class }} {{ get('size', '') }}">
        {{ adherence }}
        <div class="tooltip right">
            {{ adherence.description }}
            % if adherence.layover:
                <div class="italics">Yet to depart</div>
            % end
        </div>
    </div>
% end
