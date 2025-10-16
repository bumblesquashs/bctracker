<div class="order-details">
    <div class="row {{ 'space-between' if livery else 'justify-center' }}">
        % if livery:
            <div style="width: 40px"></div>
        % end
        <div class="column center">
            <div class="title">{{! order }}</div>
            <div class="content lighter-text smaller-font">
                % if len(order.vehicles) == 1:
                    1 {{ context.vehicle_type.lower() }}
                % else:
                    {{ len(order.vehicles) }} {{ context.vehicle_type_plural.lower() }}
                % end
            </div>
        </div>
        % if livery:
            <div>
                % include('components/livery')
            </div>
        % end
    </div>
    % if len(order.vehicles) > 1:
        <div class="content centered">
            % first_vehicle = order.vehicles[0]
            % if vehicle > first_vehicle:
                % include('components/vehicle', vehicle=first_vehicle)
                
                % previous_vehicle = order.previous_vehicle(vehicle)
                % if previous_vehicle > first_vehicle:
                    % include('components/svg', name='paging/left-triple')
                    % include('components/vehicle', vehicle=previous_vehicle)
                % end
                % include('components/svg', name='paging/left')
            % end
            
            % include('components/vehicle', enable_link=False)
            
            % last_vehicle = order.vehicles[-1]
            % if vehicle < last_vehicle:
                % include('components/svg', name='paging/right')
                % next_vehicle = order.next_vehicle(vehicle)
                % if next_vehicle < last_vehicle:
                    % include('components/vehicle', vehicle=next_vehicle)
                    % include('components/svg', name='paging/right-triple')
                % end
                % include('components/vehicle', vehicle=last_vehicle)
            % end
        </div>
    % end
</div>
