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
    % include('components/systems')
% else:
    % blocks = system.get_blocks()
    % service_groups = sorted({ s for b in blocks for s in b.service_groups })
    
    % if len(service_groups) > 1:
        % include('components/service_group_navigation', service_groups=service_groups)
    % end
    
    <div class="container">
        % for service_group in service_groups:
            <div class="section" id="{{ hash(service_group) }}">
                <h2 class="title">{{ service_group.schedule }}</h2>
                <div class="subtitle">{{ service_group }}</div>
                <table class="striped">
                    <thead>
                        <tr>
                            <th>Block</th>
                            <th>Routes</th>
                            <th class="desktop-only">Start Time</th>
                            <th class="desktop-only">End Time</th>
                            <th class="desktop-only">Duration</th>
                            <th class="non-desktop">Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        % service_group_blocks = [b for b in blocks if service_group in b.service_groups]
                        % for block in service_group_blocks:
                            % start_time = block.get_start_time(service_group)
                            % end_time = block.get_end_time(service_group)
                            <tr>
                                <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                <td>{{ block.get_routes_string(service_group) }}</td>
                                <td class="desktop-only">{{ start_time }}</td>
                                <td class="desktop-only">{{ end_time }}</td>
                                <td class="desktop-only">{{ block.get_duration(service_group) }}</td>
                                <td class="non-desktop">{{ start_time }} - {{ end_time }}</td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        % end
    </div>
% end

% include('components/top_button')
