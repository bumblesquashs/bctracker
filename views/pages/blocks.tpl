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
    % blocks = system.get_blocks(None)
    % services = sorted({ s for b in blocks for s in b.get_services(None) })
    
    <div class="container">
        % if len(services) > 1:
            <div class="navigation">
                % for service in services:
                    <a href="#{{service}}" class='button'>{{ service }}</a>
                % end
            </div>
            <br />
        % end
        
        % for service in services:
            <div class="section">
                <h2 class="title" id="{{service}}">{{ service }}</h2>
                <div class="subtitle">{{ service.date_string }}</div>
                <table class="pure-table pure-table-horizontal pure-table-striped">
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
                        % service_blocks = [block for block in blocks if service in block.get_services(None)]
                        % for block in service_blocks:
                            <tr>
                                <td><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                <td>{{ block.get_routes_string(None) }}</td>
                                <td class="desktop-only">{{ block.get_start_time(None) }}</td>
                                <td class="desktop-only">{{ block.get_end_time(None) }}</td>
                                <td class="desktop-only">{{ block.get_duration(None) }}</td>
                                <td class="non-desktop">{{ block.get_start_time(None) }} - {{ block.get_end_time(None) }}</td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        % end
    </div>
% end

% include('components/top_button')
