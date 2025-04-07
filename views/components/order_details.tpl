% order = bus.order
<div class="order-details">
    <div class="title">{{! order }}</div>
    <div class="content">
        % if bus.number > order.low:
            % first_bus = order.first_bus
            % previous_bus = order.previous_bus(bus.number)
            % include('components/bus', bus=first_bus)
            % if previous_bus.number > order.low:
                % include('components/svg', name='paging/left-triple')
                % include('components/bus', bus=previous_bus)
            % end
            % include('components/svg', name='paging/left')
        % end
        
        % include('components/bus', enable_link=False)
        
        % if bus.number < order.high:
            % last_bus = order.last_bus
            % next_bus = order.next_bus(bus.number)
            % include('components/svg', name='paging/right')
            % if next_bus.number < order.high:
                 % include('components/bus', bus=next_bus)
                 % include('components/svg', name='paging/right-triple')
            % end
            % include('components/bus', bus=last_bus)
        % end
    </div>
</div>
