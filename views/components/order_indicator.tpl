% order = bus.order
<div class="order-indicator">
    <div class="title">{{ order }}</div>
    <div class="content">
        % if bus.number > order.low:
            % low_bus = Bus(order.low)
            <a href="{{ get_url(system, f'bus/{low_bus.number}') }}" class="bus">{{ low_bus }}</a>
            % if bus.number - 1 > order.low:
                <span class="separator">&lt;&lt;&lt;</span>
                % previous_bus = Bus(bus.number - 1)
                <a href="{{ get_url(system, f'bus/{previous_bus.number}') }}" class="bus">{{ previous_bus }}</a>
            % end
            <span class="separator">&lt;</span>
        % end
        
        <span class="bus">{{ bus }}</span>
        
        % if bus.number < order.high:
            <span class="separator">&gt;</span>
            % if bus.number + 1 < order.high:
                % next_bus = Bus(bus.number + 1)
                <a href="{{ get_url(system, f'bus/{next_bus.number}') }}" class="bus">{{ next_bus }}</a>
                <span class="separator">&gt;&gt;&gt;</span>
            % end
            % high_bus = Bus(order.high)
            <a href="{{ get_url(system, f'bus/{high_bus.number}') }}" class="bus">{{ high_bus }}</a>
        % end
    </div>
</div>
