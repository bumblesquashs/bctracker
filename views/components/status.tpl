<div class="status tooltip-anchor {{ get('status_class', '') }}">
    % include('components/svg', name=icon)
    % if defined('tooltip'):
        <div class="tooltip right">{{ tooltip }}</div>
    % end
</div>
