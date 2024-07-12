
<style>
    .percentage {
        cursor: default;
        padding: 1px 4px;
        border-radius: 4px;
        background-color: #ABABAB;
    }
    
    .percentage.low {
        background-color: #FF7F7F;
    }
    
    .percentage.mid {
        background-color: #FFA560;
    }
    
    .percentage.high {
        background-color: #7DBD88;
    }
</style>

% if denominator == 0:
    <div class="percentage tooltip-anchor">
        {{ numerator }} / {{ denominator }}
        <div class="tooltip right">???</div>
    </div>
% else:
    % percentage = (numerator / denominator) * 100
    % low_cutoff = get('low_cutoff', 25)
    % high_cutoff = get('high_cutoff', 75)
    % if percentage < low_cutoff:
        % percentage_class = 'low'
    % elif percentage >= high_cutoff:
        % percentage_class = 'high'
    % else:
        % percentage_class = 'mid'
    % end   
    <div class="percentage {{ percentage_class }} tooltip-anchor">
        {{ numerator }} / {{ denominator }}
        <div class="tooltip right">
            % percentage_rounded = round(percentage, 2)
            % if percentage_rounded % 1 == 0:
                % percentage_rounded = int(percentage_rounded)
            % end
            {{ percentage_rounded }}%
        </div>
    </div>
% end
