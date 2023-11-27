<span class="tooltip-anchor">
    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.short_id }}</a>
    % if get('include_tooltip', True):
        <div class="tooltip">
            {{ trip.id }}
        </div>
    % end
</span>
