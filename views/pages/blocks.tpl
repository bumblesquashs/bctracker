
% rebase('base', title='Blocks')

<div class="page-header">
    <h1 class="title">Blocks</h1>
    <hr />
</div>

% if system is None:
    <p>
        Blocks can only be viewed for individual systems.
        Please choose a system.
    </p>
% else:
    % blocks = system.get_blocks()
    % if len(blocks) == 0:
        <p>
            Block information is currently unavailable for {{ system }}.
            Please check again later!
        </p>
    % else:
        % sheets = system.get_sheets()
        
        % if len(sheets) > 1 or (len(sheets) == 1 and len(sheets[0].service_groups) > 1):
            % include('components/sheet_navigation', sheets=sheets)
        % end
        
        <div class="container">
            % for sheet in sheets:
                % for service_group in sheet.service_groups:
                    <div class="section" id="{{ service_group.id }}">
                        <h2 class="title">{{ service_group }}</h2>
                        <div class="subtitle">{{ service_group.date_string }}</div>
                        <table class="striped">
                            <thead>
                                <tr>
                                    <th>Block</th>
                                    <th>Routes</th>
                                    <th class="non-mobile">Start Time</th>
                                    <th class="non-mobile">End Time</th>
                                    <th class="mobile-only">Time</th>
                                    <th class="desktop-only">Duration</th>
                                </tr>
                            </thead>
                            <tbody>
                                % service_group_blocks = [b for b in blocks if len(b.get_trips(service_group)) > 0]
                                % for block in service_group_blocks:
                                    % start_time = block.get_start_time(service_group)
                                    % end_time = block.get_end_time(service_group)
                                    <tr>
                                        <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                        <td>{{ block.get_routes_string(service_group) }}</td>
                                        <td class="non-mobile">{{ start_time }}</td>
                                        <td class="non-mobile">{{ end_time }}</td>
                                        <td class="mobile-only">{{ start_time }} - {{ end_time }}</td>
                                        <td class="desktop-only">{{ block.get_duration(service_group) }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    </div>
                % end
            % end
        </div>
        
        % include('components/top_button')
    % end
% end
