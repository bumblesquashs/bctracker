
% if occupancy:
    <div class="occupancy-icon {{ occupancy.status_class }} {{ get('size', '') }} tooltip-anchor">
        % include('components/svg', name=occupancy.icon)
        % if get('show_tooltip', False):
            <div class="tooltip right">{{ occupancy }}</div>
        % end
    </div>
% end
