<div class="sheet-navigation">
    % for sheet in sheets:
        % regular_service_groups = [g for g in sheet.service_groups if not g.special]
        % special_service_groups = [g for g in sheet.service_groups if g.special]
        <div class="info-box">
            <div class="section no-flex">
                <div class="service-indicator">
                    <div class="title">{{ sheet }}</div>
                </div>
            </div>
            % if len(regular_service_groups) > 0:
                <div class="section">
                    <div class="name">Regular Service</div>
                    <div class="value">
                        % for service_group in regular_service_groups:
                            <a href="#{{ service_group.id }}">{{ service_group }}</a>
                            <br />
                        % end
                    </div>
                </div>
            % end
            % if len(special_service_groups) > 0:
                <div class="section">
                    <div class="name">Special Service</div>
                    <div class="value">
                        % for service_group in special_service_groups:
                            <a href="#{{ service_group.id }}">{{ service_group.date_string }}</a>
                            <br />
                        % end
                    </div>
                </div>
            % end
        </div>
    % end
</div>
