
% import repositories

% rebase('base')

<div id="page-header">
    <h1>Trip {{! trip.display_id }}</h1>
    <h2>
        % if trip.custom_headsigns:
            % include('components/custom_headsigns', custom_headsigns=trip.custom_headsigns)
        % else:
            {{ trip }}
        % end
    </h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ trip.url('map') }}" class="tab-button">Map</a>
        % if context.config.realtime_enabled and context.config.enable_realtime_trips:
            <a href="{{ trip.url('history') }}" class="tab-button">History</a>
        % end
    </div>
</div>

% departures = trip.find_departures()

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this, true)">
                <h2>Overview</h2>
                % include('components/toggle')
            </div>
            <div class="content gap-20">
                % include('components/map', map_trip=trip, map_positions=positions)
                
                <div class="info-box">
                    <div class="section">
                        % include('components/sheet_list', sheets=trip.sheets)
                    </div>
                    <div class="section">
                        % route = trip.route
                        % if route:
                            <div class="row">
                                % include('components/route')
                                <a href="{{ route.url() }}">{{! route.display_name }}</a>
                            </div>
                        % else:
                            <div class="lighter-text">Unknown Route</div>
                        % end
                    </div>
                    % if context.config.enable_blocks:
                        % block = trip.block
                        % if block:
                            <div class="section">
                                % include('components/block_timeline', block=trip.block)
                            </div>
                        % end
                        <div class="row section">
                            <div class="name">Block</div>
                            <div class="value">
                                % if block:
                                    <a href="{{ block.url() }}">{{ block.id }}</a>
                                % else:
                                    <span class="lighter-text">Loading</span>
                                % end
                            </div>
                        </div>
                    % end
                    <div class="row section">
                        <div class="name">Start time</div>
                        <div class="value">{{ trip.start_time.format_web(time_format) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">End time</div>
                        <div class="value">{{ trip.end_time.format_web(time_format) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Duration</div>
                        <div class="value">{{ trip.duration }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Number of stops</div>
                        <div class="value">{{ len(departures) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Direction</div>
                        <div class="value">{{ trip.direction }}</div>
                    </div>
                    % length = trip.length
                    % if length is not None:
                        % km = length / trip.context.config.distance_scale
                        % hours = (float(trip.end_time.get_minutes() - trip.start_time.get_minutes())) / 60
                        <div class="row section">
                            <div class="name">Length</div>
                            <div class="value">{{ f'{km:.1f}' }}km</div>
                        </div>
                        <div class="row section">
                            <div class="name">Average Speed</div>
                            <div class="value">{{ f'{(km / hours):.1f}' }}km/h</div>
                        </div>
                        <div class="row section">
                            <div class="name">Stop Density</div>
                            <div class="value">
                                % density = len(departures) / km
                                {{ f'{density:.2f}' }}
                                % if density == 1:
                                    stop/km
                                % else:
                                    stops/km
                                % end
                            </div>
                        </div>
                    % end
                </div>
            </div>
        </div>
        
        % related_trips = trip.related_trips
        % if related_trips:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Related Trips</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Trip</th>
                                % if context.config.enable_blocks:
                                    <th class="non-mobile">Block</th>
                                % end
                                <th>Service Days</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for related_trip in related_trips:
                                % block = related_trip.block
                                <tr>
                                    <td>
                                        % include('components/trip', trip=related_trip)
                                    </td>
                                    % if context.config.enable_blocks:
                                        <td class="non-mobile">
                                            % if block:
                                                <a href="{{ block.url() }}">{{ block.id }}</a>
                                            % else:
                                                <div class="lighter-text">Unknown</div>
                                            % end
                                        </td>
                                    % end
                                    <td>
                                        <div class="column">
                                            % for sheet in related_trip.sheets:
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
                <div class="header" onclick="toggleSection(this)">
                    <h2>Active {{ context.format_model_category(count=len(positions)) }}</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>{{ context.format_model_category() }}</th>
                                <th class="non-mobile">Model</th>
                                <th>Next Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for position in sorted(positions):
                                % vehicle = position.vehicle
                                % trip = position.trip
                                % stop = position.stop
                                <tr>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % include('components/vehicle')
                                                <div class="row gap-5">
                                                    % if position.context.show_occupancy:
                                                        % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                    % end
                                                    % include('components/adherence', adherence=position.adherence)
                                                </div>
                                            </div>
                                            <span class="mobile-only smaller-font">
                                                % include('components/year_model', year_model=vehicle.year_model)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/year_model', year_model=vehicle.year_model)
                                    </td>
                                    <td>
                                        % include('components/stop')
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % elif assignment and trip.service.schedule.is_today and trip.end_time.is_later:
            % vehicle = assignment.vehicle
            % position = repositories.position.find(vehicle.agency.id, vehicle.id)
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Scheduled {{ context.format_model_category() }}</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if show_help_text:
                        <p>This {{ str(vehicle.model_category).lower() }} is currently assigned to this trip's block but may be swapped off before this trip runs.</p>
                    % end
                    <div class="table-border-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>{{ context.format_model_category() }}</th>
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
                                                % include('components/vehicle')
                                                % if position:
                                                    % include('components/adherence', adherence=position.adherence)
                                                % end
                                            </div>
                                            <span class="mobile-only smaller-font">
                                                % include('components/year_model', year_model=vehicle.year_model)
                                            </span>
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % include('components/year_model', year_model=vehicle.year_model)
                                    </td>
                                    % if position:
                                        % position_trip = position.trip
                                        % stop = position.stop
                                        % if position_trip:
                                            <td>
                                                <div class="column">
                                                    % include('components/headsign', departure=position.departure, trip=position_trip)
                                                    <div class="non-desktop smaller-font">
                                                        Trip:
                                                        % include('components/trip', include_tooltip=False, trip=position_trip)
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
                                                % include('components/trip', include_tooltip=False, trip=position_trip)
                                            </td>
                                        % else:
                                            <td colspan="2">
                                                <div class="column">
                                                    <div class="lighter-text">Not In Service</div>
                                                    % if stop:
                                                        <div class="mobile-only smaller-font">
                                                            <span class="align-middle">Next Stop:</span>
                                                            % include('components/stop')
                                                        </div>
                                                    % end
                                                </div>
                                            </td>
                                        % end
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
            </div>
        % end
        
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Stop Schedule</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="options-container">
                    <div class="option" onclick="toggleConnections()">
                        <div class="checkbox {{ 'selected' if show_connections else '' }}">
                            % include('components/svg', name='status/check')
                        </div>
                        <div>Show Connections</div>
                    </div>
                    <script>
                        function toggleConnections() {
                            storeCurrentScrollPosition();
                            window.location = "{{! trip.url(show_connections='false' if show_connections else 'true') }}";
                        }
                    </script>
                </div>
                % if any(d.timepoint for d in departures) and show_help_text:
                    <p>Departures in <span class="timing-point">bold</span> are timing points.</p>
                % end
                % last_headsign = None
                % has_other_routes = any(d.other_routes for d in departures)
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Stop</th>
                            % if show_connections and has_other_routes:
                                <th class="non-mobile">Connections</th>
                            % end
                        </tr>
                    </thead>
                    <tbody>
                        % for departure in departures:
                            % stop = departure.stop
                            % if trip.custom_headsigns:
                                % if departure.headsign != last_headsign:
                                    <tr class="header">
                                        <td colspan="{{ '3' if has_other_routes else '2' }}">{{ departure }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                % end
                                % last_headsign = departure.headsign
                            % end
                            % other_routes = departure.other_routes
                            <tr>
                                <td class="{{ 'timing-point' if departure.timepoint else '' }}">
                                    {{ departure.time.format_web(time_format) }}
                                </td>
                                <td>
                                    <div class="column">
                                        % include('components/stop', timepoint=departure.timepoint)
                                        % if show_connections and other_routes:
                                            <div class="mobile-only">
                                                % include('components/route_list', routes=other_routes)
                                            </div>
                                        % end
                                        % if not departure.pickup_type.is_normal:
                                            <span class="smaller-font italics">{{ departure.pickup_type }}</span>
                                        % elif departure == departures[-1]:
                                            <span class="smaller-font italics">No pick up</span>
                                        % end
                                        % if not departure.dropoff_type.is_normal:
                                            <span class="smaller-font italics">{{ departure.dropoff_type }}</span>
                                        % elif departure == departures[0]:
                                            <span class="smaller-font italics">No drop off</span>
                                        % end
                                    </div>
                                </td>
                                % if show_connections and has_other_routes:
                                    <td class="non-mobile">
                                        % if other_routes:
                                            % include('components/route_list', routes=other_routes)
                                        % end
                                    </td>
                                % end
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
