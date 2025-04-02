
% from models.date import Date
% from repositories import PositionRepository

% rebase('base')

<div id="page-header">
    <h1>Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, 'blocks', block, 'map') }}" class="tab-button">Map</a>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, 'blocks', block, 'history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% sheets = block.sheets
% routes = block.get_routes()
% trips = block.get_trips()

% today = Date.today(block.system.timezone)

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Overview</h2>
                % include('components/toggle')
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
                                <a href="{{ get_url(route.system, 'routes', route) }}">{{! route.display_name }}</a>
                            </div>
                        % end
                    </div>
                    % for sheet in sheets:
                        % service_groups = sheet.service_groups
                        % if service_groups:
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
                            % if [t for t in block.get_trips() if t.length is not None]:
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
        % if related_blocks:
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
                                    <td><a href="{{ get_url(related_block.system, 'blocks', related_block) }}">{{ related_block.id }}</a></td>
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
        % if positions:
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
                                                <div class="row gap-5">
                                                    % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                    % include('components/adherence', adherence=position.adherence)
                                                </div>
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
                                            % if stop:
                                                <div class="mobile-only smaller-font">
                                                    <span class="align-middle">Next Stop:</span>
                                                    % include('components/stop')
                                                </div>
                                            % end
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/trip')
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/stop')
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % elif assignment and block.schedule.is_today and block.get_end_time(date=today).is_later:
            % bus = assignment.bus
            % position = di[PositionRepository].find(bus.agency, bus)
            <div class="section">
                <div class="header">
                    <h2>Scheduled Bus</h2>
                </div>
                <div class="content">
                    <p>This bus is currently assigned to this block but may be swapped off.</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="non-mobile">Model</th>
                                <th>Current Headsign</th>
                                <th class="desktop-only">Current Trip</th>
                                <th class="non-mobile">Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <div class="column">
                                        <div class="row">
                                            % include('components/bus')
                                            % if position:
                                                % include('components/adherence', adherence=position.adherence)
                                            % end
                                        </div>
                                        <span class="mobile-only smaller-font">
                                            % include('components/order', order=bus.order)
                                        </span>
                                    </div>
                                </td>
                                <td class="non-mobile">
                                    % include('components/order', order=bus.order)
                                </td>
                                % if position and position.trip:
                                    % stop = position.stop
                                    <td>
                                        <div class="column">
                                            % include('components/headsign', trip=position.trip)
                                            <div class="non-desktop smaller-font">
                                                Trip:
                                                % include('components/trip', include_tooltip=False, trip=position.trip)
                                            </div>
                                            % if stop:
                                                <div class="mobile-only smaller-font">
                                                    <span class="align-middle">Next Stop:</span>
                                                    % include('components/stop')
                                                </div>
                                            % end
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/trip', include_tooltip=False, trip=position.trip)
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/stop')
                                    </td>
                                % else:
                                    <td class="lighter-text" colspan="3">Not In Service</td>
                                % end
                            </tr>
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
