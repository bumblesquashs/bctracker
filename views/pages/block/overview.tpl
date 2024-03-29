
% rebase('base')

<div id="page-header">
    <h1>Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'blocks/{block.id}/map') }}" class="tab-button">Map</a>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'blocks/{block.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% sheets = block.sheets
% routes = block.get_routes()
% trips = block.get_trips()

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Overview</h2>
            </div>
            <div class="content">
                % include('components/map', map_trips=trips, map_positions=positions)
                
                <div class="info-box">
                    <div class="section">
                        % include('components/sheet_list')
                    </div>
                    <div class="column section">
                        % for route in routes:
                            <div class="row">
                                % include('components/route')
                                <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                            </div>
                        % end
                    </div>
                    % for sheet in sheets:
                        % service_groups = sheet.service_groups
                        % if len(service_groups) > 0:
                            % if len(sheets) > 1:
                                <div class="title">
                                    <h3>{{ sheet }}</h3>
                                </div>
                            % end
                            % for service_group in service_groups:
                                <div class="section">
                                    % if len(service_groups) > 1:
                                        <div class="lighter-text">{{ service_group }}</div>
                                    % end
                                    % include('components/block_timeline', service_group=service_group)
                                </div>
                            % end
                            <div class="row section">
                                <div class="name">Start time</div>
                                <div class="value">
                                    % for service_group in service_groups:
                                        <div>
                                            % if len(service_groups) > 1:
                                                <div class="smaller-font lighter-text">{{ service_group }}</div>
                                            % end
                                            <div>{{ block.get_start_time(service_group=service_group).format_web(time_format) }}</div>
                                        </div>
                                    % end
                                </div>
                            </div>
                            <div class="row section">
                                <div class="name">End time</div>
                                <div class="value">
                                    % for service_group in service_groups:
                                        <div>
                                            % if len(service_groups) > 1:
                                                <div class="smaller-font lighter-text">{{ service_group }}</div>
                                            % end
                                            <div>{{ block.get_end_time(service_group=service_group).format_web(time_format) }}</div>
                                        </div>
                                    % end
                                </div>
                            </div>
                            <div class="row section">
                                <div class="name">Duration</div>
                                <div class="value">
                                    % for service_group in service_groups:
                                        <div>
                                            % if len(service_groups) > 1:
                                                <div class="smaller-font lighter-text">{{ service_group }}</div>
                                            % end
                                            <div>{{ block.get_duration(service_group=service_group) }}</div>
                                        </div>
                                    % end
                                </div>
                            </div>
                            <div class="row section">
                                <div class="name">Number of trips</div>
                                <div class="value">
                                    % for service_group in service_groups:
                                        <div>
                                            % if len(service_groups) > 1:
                                                <div class="smaller-font lighter-text">{{ service_group }}</div>
                                            % end
                                            <div>{{ len(block.get_trips(service_group=service_group)) }}</div>
                                        </div>
                                    % end
                                </div>
                            </div>
                            % if len([t for t in block.get_trips() if t.length is not None]) > 0:
                                <div class="row section">
                                    <div class="name">Length</div>
                                    <div class="value">
                                        % for service_group in service_groups:
                                            <div>
                                                % if len(service_groups) > 1:
                                                    <div class="smaller-font lighter-text">{{ service_group }}</div>
                                                % end
                                                % length = sum([t.length for t in block.get_trips(service_group=service_group) if t.length is not None])
                                                <div class="value">{{ f'{(length / 1000):.1f}' }}km</div>
                                            </div>
                                        % end
                                    </div>
                                </div>
                            % end
                        % end
                    % end
                </div>
            </div>
        </div>
        
        % related_blocks = block.related_blocks
        % if len(related_blocks) > 0:
            <div class="section">
                <div class="header">
                    <h2>Related Blocks</h2>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Block</th>
                                <th>Service Days</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for related_block in related_blocks:
                                <tr>
                                    <td><a href="{{ get_url(related_block.system, f'blocks/{related_block.id}') }}">{{ related_block.id }}</a></td>
                                    <td>
                                        <div class="column">
                                            % for sheet in related_block.sheets:
                                                <div>{{ sheet }}</div>
                                                <div class="smaller-font lighter-text">{{ sheet.schedule }}</div>
                                            % end
                                        </div>
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
    </div>
    
    <div class="container flex-3">
        % if len(positions) > 0:
            <div class="section">
                <div class="header">
                    % if len(positions) == 1:
                        <h2>Active Bus</h2>
                    % else:
                        <h2>Active Buses</h2>
                    % end
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="desktop-only">Model</th>
                                <th>Headsign</th>
                                <th class="non-mobile">Trip</th>
                                <th class="non-mobile">Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for position in sorted(positions):
                                % bus = position.bus
                                % trip = position.trip
                                % stop = position.stop
                                <tr>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % include('components/bus')
                                                % include('components/adherence', adherence=position.adherence)
                                            </div>
                                            <span class="non-desktop smaller-font">
                                                % include('components/order', order=bus.order)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/order', order=bus.order)
                                    </td>
                                    <td>
                                        <div class="column">
                                            % include('components/headsign')
                                            <div class="mobile-only smaller-font">
                                                Trip:
                                                % include('components/trip', include_tooltip=False)
                                            </div>
                                            % if stop is not None:
                                                <div class="mobile-only smaller-font">
                                                    Next Stop: <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                                </div>
                                            % end
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/trip')
                                    </td>
                                    <td class="non-mobile">
                                        % if stop is None:
                                            <span class="lighter-text">Unavailable</span>
                                        % else:
                                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                        % end
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
        
        <div class="section">
            <div class="header">
                <h2>Trip Schedule</h2>
            </div>
            <div class="content">
                <div class="container inline">
                    % for sheet in sheets:
                        <div class="section">
                            % if len(sheets) > 1:
                                <div class="header">
                                    <h3>{{ sheet }}</h3>
                                </div>
                            % end
                            <div class="content">
                                <div class="container inline">
                                    % service_groups = sheet.service_groups
                                    % for service_group in service_groups:
                                        % service_group_trips = block.get_trips(service_group=service_group)
                                        <div class="section">
                                            % if len(service_groups) > 1:
                                                <div class="header">
                                                    <h4>{{ service_group }}</h4>
                                                </div>
                                            % end
                                            <div class="content">
                                                <table>
                                                    <thead>
                                                        <tr>
                                                            <th>Start Time</th>
                                                            <th class="non-mobile">End Time</th>
                                                            <th class="desktop-only">Duration</th>
                                                            <th class="non-mobile">Headsign</th>
                                                            <th class="desktop-only">Direction</th>
                                                            <th>Trip</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        % for trip in service_group_trips:
                                                            <tr>
                                                                <td>{{ trip.start_time.format_web(time_format) }}</td>
                                                                <td class="non-mobile">{{ trip.end_time.format_web(time_format) }}</td>
                                                                <td class="desktop-only">{{ trip.duration }}</td>
                                                                <td class="non-mobile">
                                                                    <div class="column">
                                                                        % include('components/headsign')
                                                                        <span class="non-desktop smaller-font">{{ trip.direction }}</span>
                                                                    </div>
                                                                </td>
                                                                <td class="desktop-only">{{ trip.direction }}</td>
                                                                <td>
                                                                    <div class="column">
                                                                        % include('components/trip')
                                                                        <span class="mobile-only smaller-font">
                                                                            % include('components/headsign')
                                                                        </span>
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        % end
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    % end
                                </div>
                            </div>
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
</div>
    
% include('components/top_button')
