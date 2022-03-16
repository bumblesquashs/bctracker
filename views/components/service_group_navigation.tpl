<div class="service-navigation">
    % special_service_groups = []
    <div class="buttons">
        % for service_group in service_groups:
            % schedule = service_group.schedule
            % if schedule.special:
                % number = str(len(special_service_groups) + 1)
                % special_service_groups.append((service_group, number))
                <a href="#{{ hash(service_group) }}" class='button'>
                    {{ schedule }}
                    <span class="special-number">{{ number }}</span>
                </a>
            % else:
                <a href="#{{ hash(service_group) }}" class='button'>{{ schedule }}</a>
            % end
        % end
    </div>
    % if len(special_service_groups) > 0:
        <h3>Special Service</h3>
        <ul class="special-services">
            % for (service_group, number) in special_service_groups:
                <li>
                    <span class="special-number">{{ number }}.</span>
                    {{ service_group }}
                </li>
            % end
        </ul>
    % end
</div>
