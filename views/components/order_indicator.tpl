% order = bus.order
<div class="order-indicator">
    <div class="title">{{ order }}</div>
    <div class="content">
        % if bus.number > order.low:
            % first_bus = order.first_bus
            % previous_bus = order.previous_bus(bus.number)
            <a href="{{ get_url(system, f'bus/{first_bus.number}') }}" class="bus">{{ first_bus }}</a>
            % if previous_bus.number > order.low:
                <span class="separator">&lt;&lt;&lt;</span>
                <a href="{{ get_url(system, f'bus/{previous_bus.number}') }}" class="bus">{{ previous_bus }}</a>
            % end
            <span class="separator">&lt;</span>
        % end
        
        <span class="bus">{{ bus }}</span>
        
        % if bus.number < order.high:
            % last_bus = order.last_bus
            % next_bus = order.next_bus(bus.number)
            <span class="separator">&gt;</span>
            % if next_bus.number < order.high:
                <a href="{{ get_url(system, f'bus/{next_bus.number}') }}" class="bus">{{ next_bus }}</a>
                <span class="separator">&gt;&gt;&gt;</span>
            % end
            <a href="{{ get_url(system, f'bus/{last_bus.number}') }}" class="bus">{{ last_bus }}</a>
        % end
    </div>
</div>
