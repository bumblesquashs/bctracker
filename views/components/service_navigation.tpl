<div class="service-navigation">
    % special_services = []
    <div class="buttons">
        % for service in get('services', []):
            % if service.special:
                % number = str(len(special_services) + 1)
                % special_services.append((service, number))
                <a href="#service-{{service.id}}" class='button'>
                    {{ service }}
                    <span class="special-number">{{ number }}</span>
                </a>
            % else:
                <a href="#service-{{service.id}}" class='button'>{{ service }}</a>
            % end
        % end
    </div>
    % if len(special_services) > 0:
        <h3>Special Service</h3>
        <ul class="special-services">
            % for (service, number) in special_services:
                <li>
                    <span class="special-number">{{ number }}.</span>
                    {{ service.date_string }}
                </li>
            % end
        </ul>
    % end
</div>
