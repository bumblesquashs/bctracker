% if adherence is not None:
    % status = 'on-time'
    % if adherence <= -8:
        % status = 'very-behind'
    % elif adherence <= -5:
        % status = 'behind'
    % elif adherence >= 5:
        % status = 'very-ahead'
    % elif adherence >= 3:
        % status = 'ahead'
    % end
    <div class="adherence-indicator {{ status }}">
        % if adherence > 0:
            +{{ adherence }}
        % else:
            {{ adherence }}
        % end
    </div>
% end