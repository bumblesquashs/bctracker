
<div class="sheet-sidebar">
    % for (i, sheet) in enumerate(sheets):
        % url_suffix = '' if i == 0 else f'{i + 1}'
        % include('components/schedule_indicator', schedule=sheet.schedule)
    % end
</div>
