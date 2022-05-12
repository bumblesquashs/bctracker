<div class="sheet-navigation">
    % for sheet in sheets:
        <div class="sheet">
            % special_service_groups = []
            % if len(sheets) > 1:
                <h3>{{ sheet }}</h3>
            % end
            <div class="buttons">
                % for service_group in sheet.service_groups:
                    % if service_group.special:
                        % number = str(len(special_service_groups) + 1)
                        % special_service_groups.append((service_group, number))
                        <a href="#{{ service_group.id }}" class='button'>
                            {{ service_group }}
                            <span class="special-number">{{ number }}</span>
                        </a>
                    % else:
                        <a href="#{{ service_group.id }}" class='button'>{{ service_group }}</a>
                    % end
                % end
            </div>
            % if len(special_service_groups) > 0:
                <b>Special Service</b>
                <ul class="special-services">
                    % for (service_group, number) in special_service_groups:
                        <li>
                            <span class="special-number">{{ number }}.</span>
                            {{ service_group.date_string }}
                        </li>
                    % end
                </ul>
            % end
        </div>
    % end
</div>
