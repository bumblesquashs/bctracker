<span class="tooltip-anchor trip">
    <a href="{{ trip.url() }}">{{ trip.short_id }}</a>
    % if get('include_tooltip', True) and trip.short_id != trip.id:
        <div class="tooltip right">{{ trip.id }}</div>
    % end
</span>
