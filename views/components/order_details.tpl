<div class="order-details">
    <div class="row space-between">
        % if livery:
            <div style="width: 40px"></div>
        % end
        <div class="column center">
            <div class="title">{{! order }}</div>
            <div class="content lighter-text smaller-font">
                % if len(order.buses) == 1:
                    1 {{ context.vehicle_type.lower() }}
                % else:
                    {{ len(order.buses) }} {{ context.vehicle_type_plural.lower() }}
                % end
            </div>
        </div>
        % if livery:
            <div>
                % include('components/livery')
            </div>
        % end
    </div>
    % if len(order.buses) > 1:
        <div class="content">
            % first_bus = order.buses[0]
            % if bus > first_bus:
                % include('components/bus', bus=first_bus)
                
                % previous_bus = order.previous_bus(bus)
                % if previous_bus > first_bus:
                    % include('components/svg', name='paging/left-triple')
                    % include('components/bus', bus=previous_bus)
                % end
                % include('components/svg', name='paging/left')
            % end
            
            % include('components/bus', enable_link=False)
            
            % last_bus = order.buses[-1]
            % if bus < last_bus:
                % include('components/svg', name='paging/right')
                % next_bus = order.next_bus(bus)
                % if next_bus < last_bus:
                    % include('components/bus', bus=next_bus)
                    % include('components/svg', name='paging/right-triple')
                % end
                % include('components/bus', bus=last_bus)
            % end
        </div>
    % end
</div>
