% trip = departure.trip
% if trip and departure != trip.last_departure:
    <a class="departure tooltip-anchor" style="border-bottom-color: #{{ trip.route.colour }};" href="{{ trip.url() }}">
        {{ f'{departure.time.minute:02}' }}
        <div class="tooltip right">
            <div class="title">{{ trip }}</div>
            <div>{{ departure.time.format_web(time_format) }}</div>
            % if get('show_stop_info', False):
                % if departure.stop:
                    <div>{{ departure.stop }}</div>
                % end
            % else:
                % if not departure.pickup_type.is_normal:
                    <div class="italics">{{ departure.pickup_type }}</div>
                % end
                % if not departure.dropoff_type.is_normal:
                    <div class="italics">{{ departure.dropoff_type }}</div>
                % end
            % end
        </div>
    </a>
% end
