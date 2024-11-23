<span class="tooltip-anchor">
    <a href="{{ get_url(trip.system, 'trips', trip) }}">{{ trip.short_id }}</a>
    % if get('include_tooltip', True) and trip.short_id != trip.id:
        <div class="tooltip right">{{ trip.id }}</div>
    % end
</span>
