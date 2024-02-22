% order = bus.order
<div class="order-details">
    <div class="title">{{! order }}</div>
    <div class="content">
        % if bus.number > order.low:
            % first_bus = order.first_bus
            % previous_bus = order.previous_bus(bus.number)
            % include('components/bus', bus=first_bus)
            % if previous_bus.number > order.low:
                <span class="separator">&lt;&lt;&lt;</span>
                % include('components/bus', bus=previous_bus)
            % end
            <span class="separator">&lt;</span>
        % end
        
        % include('components/bus', enable_link=False)
        
        % if bus.number < order.high:
            % last_bus = order.last_bus
            % next_bus = order.next_bus(bus.number)
            <span class="separator">&gt;</span>
            % if next_bus.number < order.high:
                 % include('components/bus', bus=next_bus)
                <span class="separator">&gt;&gt;&gt;</span>
            % end
            % include('components/bus', bus=last_bus)
        % end
    </div>
</div>
