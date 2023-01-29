
% rebase('base', title=f'Block {block.id}', include_maps=True)

<div class="page-header">
    <h1 class="title">Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'blocks/{block.id}/map') }}" class="tab-button">Map</a>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'blocks/{block.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
    <hr />
</div>

% sheets = block.sheets
% service_groups = sorted({g for s in sheets for g in s.service_groups})
% routes = block.get_routes()
% trips = block.get_trips()

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div>
            <h2>Overview</h2>
            % include('components/map', map_trips=trips, map_positions=positions)
            
            <div class="info-box">
                <div class="section no-flex">
                    % include('components/schedules_indicator', schedules=[s.schedule for s in sheets])
                </div>
                <div class="section">
                    <div class="name">Start time</div>
                    <div class="value">
                        % for service_group in service_groups:
                            % if len(service_groups) > 1:
                                <div class="smaller-font lighter-text">
                                    % if len(sheets) > 1:
                                        {{ service_group.schedule.date_string }}
                                    % else:
                                        {{ service_group }}
                                    % end
                                </div>
                            % end
                            <div>{{ block.get_start_time(service_group=service_group).format_web(time_format) }}</div>
                        % end
                    </div>
                </div>
                <div class="section">
                    <div class="name">End time</div>
                    <div class="value">
                        % for service_group in service_groups:
                            % if len(service_groups) > 1:
                                <div class="smaller-font lighter-text">
                                    % if len(sheets) > 1:
                                        {{ service_group.schedule.date_string }}
                                    % else:
                                        {{ service_group }}
                                    % end
                                </div>
                            % end
                            <div>{{ block.get_end_time(service_group=service_group).format_web(time_format) }}</div>
                        % end
                    </div>
                </div>
                <div class="section">
                    <div class="name">Duration</div>
                    <div class="value">
                        % for service_group in service_groups:
                            % if len(service_groups) > 1:
                                <div class="smaller-font lighter-text">
                                    % if len(sheets) > 1:
                                        {{ service_group.schedule.date_string }}
                                    % else:
                                        {{ service_group }}
                                    % end
                                </div>
                            % end
                            <div>{{ block.get_duration(service_group=service_group) }}</div>
                        % end
                    </div>
                </div>
                <div class="section">
                    <div class="name">Number of trips</div>
                    <div class="value">
                        % for service_group in service_groups:
                            % if len(service_groups) > 1:
                                <div class="smaller-font lighter-text">
                                    % if len(sheets) > 1:
                                        {{ service_group.schedule.date_string }}
                                    % else:
                                        {{ service_group }}
                                    % end
                                </div>
                            % end
                            <div>{{ len(block.get_trips(service_group=service_group)) }}</div>
                        % end
                    </div>
                </div>
                <div class="section">
                    <div class="name">Route{{ '' if len(routes) == 1 else 's' }}</div>
                    <div class="value">
                        % for route in routes:
                            <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
                            <br />
                        % end
                    </div>
                </div>
            </div>
        </div>
        
        % related_blocks = block.related_blocks
        % if len(related_blocks) > 0:
            <div>
                <h2>Related Blocks</h2>
                <table class="striped">
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
                                <td>{{ related_block.schedule }}</td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        % end
    </div>
    
    <div class="container flex-3">
        % if len(positions) > 0:
            <div>
                <h2>Active Bus{{ '' if len(positions) == 1 else 'es' }}</h2>
                <table class="striped">
                    <thead>
                        <tr>
                            <th>Bus</th>
                            <th class="desktop-only">Model</th>
                            <th class="desktop-only">Headsign</th>
                            <th>Trip</th>
                            <th class="non-mobile">Next Stop</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for position in sorted(positions):
                            % bus = position.bus
                            % order = bus.order
                            % trip = position.trip
                            % stop = position.stop
                            <tr>
                                <td>
                                    <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                    <br class="non-desktop" />
                                    <span class="non-desktop smaller-font">
                                        % if order is None:
                                            <span class="lighter-text">Unknown Year/Model</span>
                                        % else:
                                            {{ order }}
                                        % end
                                    </span>
                                </td>
                                <td class="desktop-only">
                                    % if order is None:
                                        <span class="lighter-text">Unknown Year/Model</span>
                                    % else:
                                        {{ order }}
                                    % end
                                </td>
                                <td class="desktop-only">{{ trip }}</td>
                                <td>
                                    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                    <br class="non-desktop" />
                                    <span class="non-desktop smaller-font">{{ trip }}</span>
                                </td>
                                % if stop is None:
                                    <td class="non-mobile lighter-text">Unavailable</td>
                                % else:
                                    <td class="non-mobile">
                                        % include('components/adherence_indicator', adherence=position.adherence)
                                        <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                    </td>
                                % end
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        % end
        
        <div>
            <h2>Trip Schedule</h2>
            <div class="container inline">
                % for sheet in sheets:
                    <div>
                        <h3>{{ sheet }}</h3>
                        <div class="container inline">
                            % for service_group in sheet.service_groups:
                                % service_group_trips = block.get_trips(service_group=service_group)
                                <div>
                                    <h4>{{ service_group }}</h4>
                                    % if service_group.schedule.special:
                                        <div class="subtitle">{{ service_group.schedule.modified_dates_string }}</div>
                                    % end
                                    <table class="striped">
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
                                                        {{ trip }}
                                                        <br class="non-desktop" />
                                                        <span class="non-desktop smaller-font">{{ trip.direction }}</span>
                                                    </td>
                                                    <td class="desktop-only">{{ trip.direction }}</td>
                                                    <td>
                                                        <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                                        <br class="mobile-only" />
                                                        <span class="mobile-only smaller-font">{{ trip }}</span>
                                                    </td>
                                                </tr>
                                            % end
                                        </tbody>
                                    </table>
                                </div>
                            % end
                        </div>
                    </div>
                % end
            </div>
        </div>
    </div>
</div>
    
% include('components/top_button')
