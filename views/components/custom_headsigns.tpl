<div class="custom-headsigns">
    <div>{{ custom_headsigns[0] }}</div>
    % if len(custom_headsigns) > 2:
        % include('components/svg', name='paging/right')
        <div class="tooltip-anchor lighter-text">
            ...
            <div class="tooltip right">
                % for headsign in custom_headsigns[1:-1]:
                    <div>{{ headsign }}</div>
                % end
            </div>
        </div>
    % end
    % if len(custom_headsigns) > 1:
        % include('components/svg', name='paging/right')
        <div>{{ custom_headsigns[-1] }}</div>
    % end
</div>
