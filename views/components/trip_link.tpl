<span class="tooltip-anchor">
    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.short_id }}</a>
    % if get('include_tooltip', True) and trip.short_id != trip.id:
        <div class="tooltip">
            {{ trip.id }}
        </div>
    % end
</span>
