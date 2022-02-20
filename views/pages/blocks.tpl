% rebase('base', title='Blocks')

<div class="page-header">
    <h1 class="title">Blocks</h1>
</div>
<hr />

% if system is None:
    <p>
        Blocks can only be viewed for individual systems.
        Please choose a system.
    </p>
    % include('components/systems')
% else:
    % blocks = system.get_blocks(sheet)
    % services = sorted({ s for b in blocks for s in b.get_services(sheet) })
    
    <div class="container">
        % if len(services) > 1:
            <div class="navigation">
                % for service in services:
                    <a href="#service-{{service.id}}" class='button'>{{ service }}</a>
                % end
            </div>
            <br />
        % end
        
        % for service in services:
            <div class="section">
                <h2 class="title" id="service-{{service.id}}">{{ service }}</h2>
                <div class="subtitle">{{ service.date_string }}</div>
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
                        % service_blocks = [b for b in blocks if service in b.get_services(sheet)]
                        % for block in service_blocks:
                            % start_time = block.get_start_time(sheet)
                            % end_time = block.get_end_time(sheet)
                            <tr>
                                <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                <td>{{ block.get_routes_string(sheet) }}</td>
                                <td class="desktop-only">{{ start_time }}</td>
                                <td class="desktop-only">{{ end_time }}</td>
                                <td class="desktop-only">{{ block.get_duration(sheet) }}</td>
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
