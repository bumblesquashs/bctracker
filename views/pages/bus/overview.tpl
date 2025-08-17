
% from datetime import timedelta

% from models.date import Date
% from models.model import ModelType

% rebase('base')

% model = bus.model

% if position and position.timestamp:
    <script>
        const originalTimestamp = parseFloat("{{ position.timestamp.value }}") * 1000;
    </script>
% end

<div id="page-header">
    <h1 class="row">
        <span>Bus</span>
        % include('components/bus', enable_link=False)
        % include('components/favourite')
    </h1>
    % year_model = bus.year_model
    % if year_model:
        <h2>{{! year_model }}</h2>
    % else:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % end
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(context, 'bus', bus, 'map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(context, 'bus', bus, 'history') }}" class="tab-button">History</a>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Realtime Information</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if position:
                    % trip = position.trip
                    % if trip:
                        % include('components/map', map_position=position, map_trip=trip, map_departures=trip.find_departures(), zoom_trips=False, zoom_departures=False)
                    % else:
                        % include('components/map', map_position=position)
                    % end
                % else:
                    % if last_position:
                        <div class="column stretch gap-10">
                            <div class="warning-box">
                                % include('components/svg', name='status/warning')
                                <p>Showing last known location, may not be current</p>
                            </div>
                            % include('components/map', map_position=last_position, outdated=True)
                        </div>
                    % end
                    % trip = None
                % end
                
                <div class="info-box">
                    <div class="section">
                        % if position and trip:
                            <div class="row">
                                % include('components/adherence', adherence=position.adherence, size='large')
                                % departure = position.departure
                                % if departure and departure.headsign:
                                    <h3>{{ departure }}</h3>
                                % else:
                                    <h3>{{ trip }}</h3>
                                % end
                            </div>
                        % else:
                            <h3>Not In Service</h3>
                        % end
                    </div>
                    % if position:
                        % stop = position.stop
                        % if trip:
                            % route = trip.route
                            % block = trip.block
                        % else:
                            % route = None
                            % block = None
                        % end
                        % if route:
                            <div class="section">
                                <div class="row">
                                    % include('components/route')
                                    <a href="{{ get_url(route.context, 'routes', route) }}">{{! route.display_name }}</a>
                                </div>
                            </div>
                        % end
                        % if context.enable_blocks and block:
                            <div class="section">
                                % include('components/block_timeline', date=Date.today(block.context.timezone))
                            </div>
                        % end
                        % if position.timestamp:
                            <div class="row section">
                                <div class="name">Last Update</div>
                                <div id="timestamp"></div>
                                <script>
                                    updateTimestampFunctions.push(function(currentTime) {
                                        const difference = getDifference(currentTime, originalTimestamp + timestampOffset);
                                        document.getElementById("timestamp").innerHTML = difference;
                                    });
                                </script>
                            </div>
                        % end
                        <div class="row section">
                            <div class="name">System</div>
                            <div class="value">
                                <a href="{{ get_url(position.context) }}">{{ position.context }}</a>
                            </div>
                        </div>
                        <div class="row section">
                            <div class="name">Occupancy</div>
                            <div class="value">
                                <div class="row gap-5 center">
                                    <div>{{ position.occupancy }}</div>
                                    % include('components/occupancy', occupancy=position.occupancy, size='large')
                                </div>
                            </div>
                        </div>
                        % if show_speed:
                            <div class="row section">
                                <div class="name">Speed</div>
                                <div class="value">{{ position.speed }} km/h</div>
                            </div>
                        % end
                        % if context.enable_blocks and block:
                            <div class="row section">
                                <div class="name">Block</div>
                                <div class="value">
                                    <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                    % date = Date.today(block.context.timezone)
                                    % start_time = block.get_start_time(date=date).format_web(time_format)
                                    % end_time = block.get_end_time(date=date).format_web(time_format)
                                    % duration = block.get_duration(date=date)
                                    <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ duration }})</span>
                                </div>
                            </div>
                        % end
                        % if trip:
                            <div class="row section">
                                <div class="name">Trip</div>
                                <div class="value">
                                    % include('components/trip')
                                    % start_time = trip.start_time.format_web(time_format)
                                    % end_time = trip.end_time.format_web(time_format)
                                    <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ trip.duration }})</span>
                                </div>
                            </div>
                        % end
                        % if stop:
                            <div class="row section">
                                <div class="name">Next Stop</div>
                                <div class="value">
                                    % include('components/stop', show_number=False)
                                    % adherence = position.adherence
                                    % if adherence:
                                        <span class="smaller-font">{{ adherence.description }}</span>
                                    % end
                                </div>
                            </div>
                        % end
                    % else:
                        <div class="row section">
                            <div class="name">Last Seen</div>
                            <div class="value">
                                % if allocation:
                                    % if allocation.last_seen.is_today:
                                        <div>Today</div>
                                    % else:
                                        <div>{{ allocation.last_seen.format_long() }}</div>
                                        <div class="smaller-font">{{ allocation.last_seen.format_since() }}</div>
                                    % end
                                % else:
                                    <div class="lighter-text">Never</div>
                                % end
                            </div>
                        </div>
                        % if allocation:
                            <div class="row section">
                                <div class="name">System</div>
                                <div class="value">
                                    <a href="{{ get_url(allocation.context) }}">{{ allocation.context }}</a>
                                </div>
                            </div>
                        % end
                    % end
                </div>
            </div>
        </div>
        
        % if order:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Details</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section">
                            % include('components/order_details')
                        </div>
                        % if model:
                            <div class="row section">
                                <div class="name">Vehicle Type</div>
                                <div class="value">{{ model.type }}</div>
                            </div>
                            % if model.length:
                                <div class="row section">
                                    <div class="name">Length</div>
                                    <div class="value">{{ model.length }} feet</div>
                                </div>
                            % end
                            % if model.fuel:
                                <div class="row section">
                                    <div class="name">Fuel Type</div>
                                    <div class="value">{{ model.fuel }}</div>
                                </div>
                            % end
                        % end
                        % if bus.has_amenities:
                            <div class="row section">
                                <div class="name">Amenities</div>
                                <div class="value">
                                    <div class="row gap-5">
                                        % if bus.accessible:
                                            <div class="tooltip-anchor amenity">
                                                % include('components/svg', name='amenities/accessible')
                                                <div class="tooltip right">Accessible</div>
                                            </div>
                                        % end
                                        % if bus.air_conditioned:
                                            <div class="tooltip-anchor amenity">
                                                % include('components/svg', name='amenities/air-conditioned')
                                                <div class="tooltip right">Air conditioned</div>
                                            </div>
                                        % end
                                        % if bus.usb_charging:
                                            <div class="tooltip-anchor amenity">
                                                % include('components/svg', name='amenities/usb')
                                                <div class="tooltip right">USB charging ports</div>
                                            </div>
                                        % end
                                        % if bus.cctv:
                                            <div class="tooltip-anchor amenity">
                                                % include('components/svg', name='amenities/cctv')
                                                <div class="tooltip right">CCTV cameras</div>
                                            </div>
                                        % end
                                    </div>
                                </div>
                            </div>
                        % end
                    </div>
                </div>
            </div>
        % end
    </div>
    
    <div class="container flex-3">
        % if position and upcoming_departures:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Upcoming Stops</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    % if any(d.timepoint for d in upcoming_departures):
                        <p>Departures in <span class="timing-point">bold</span> are timing points.</p>
                    % end
                    % if position.adherence and position.adherence.value != 0 and not position.adherence.layover:
                        <p>Times in brackets are estimates based on current location.</p>
                    % end
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Stop</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for departure in upcoming_departures[:5]:
                                % include('rows/upcoming_departure')
                            % end
                            % if len(upcoming_departures) > 5:
                                <tr id="show-all-upcoming-stops-button" class="table-button" onclick="showAllUpcomingStops()">
                                    <td colspan="2">
                                        <div class="row justify-center">
                                            % include('components/svg', name='action/open')
                                            Show Full Schedule
                                        </div>
                                    </td>
                                </tr>
                                <tr class="display-none"></tr>
                                % for departure in upcoming_departures[5:]:
                                    % include('rows/upcoming_departure', hidden=True)
                                % end
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
            <script>
                function showAllUpcomingStops() {
                    document.getElementById("show-all-upcoming-stops-button").classList.add("display-none");
                    for (const element of document.getElementsByClassName("table-button-target")) {
                        element.classList.remove("display-none");
                    }
                }
            </script>
        % end
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Recent History</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if records:
                    % if any(r.warnings for r in records):
                        <p>
                            <span>Entries with a</span>
                            <span class="record-warnings">
                                % include('components/svg', name='status/warning')
                            </span>
                            <span>may be accidental logins.</span>
                        </p>
                    % end
                    <div class="table-border-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th class="desktop-only">System</th>
                                    % if context.enable_blocks:
                                        <th>Block</th>
                                        <th class="desktop-only">Routes</th>
                                    % else:
                                        <th>Routes</th>
                                    % end
                                    <th class="desktop-only">Start Time</th>
                                    <th class="desktop-only">End Time</th>
                                    <th class="no-wrap non-mobile">First Seen</th>
                                    <th class="no-wrap">Last Seen</th>
                                </tr>
                            </thead>
                            <tbody>
                                % last_date = None
                                % for record in records:
                                    % if not last_date or record.date.year != last_date.year or record.date.month != last_date.month:
                                        <tr class="header">
                                            <td colspan="8">{{ record.date.format_month() }}</td>
                                            <tr class="display-none"></tr>
                                        </tr>
                                    % end
                                    % last_date = record.date
                                    <tr>
                                        <td>
                                            <div class="column">
                                                {{ record.date.format_day() }}
                                                <span class="non-desktop smaller-font">{{ record.context }}</span>
                                            </div>
                                        </td>
                                        <td class="desktop-only">{{ record.context }}</td>
                                        % if context.enable_blocks:
                                            <td>
                                                <div class="column stretch">
                                                    <div class="row space-between">
                                                        % if record.is_available:
                                                            % block = record.block
                                                            <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                                        % else:
                                                            <span>{{ record.block_id }}</span>
                                                        % end
                                                        % include('components/record_warnings')
                                                    </div>
                                                    <div class="non-desktop">
                                                        % include('components/route_list', routes=record.routes)
                                                    </div>
                                                </div>
                                            </td>
                                            <td class="desktop-only">
                                                % include('components/route_list', routes=record.routes)
                                            </td>
                                        % else:
                                            <td>
                                                % include('components/route_list', routes=record.routes)
                                            </td>
                                        % end
                                        <td class="desktop-only">{{ record.start_time.format_web(time_format) }}</td>
                                        <td class="desktop-only">{{ record.end_time.format_web(time_format) }}</td>
                                        <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                        <td>{{ record.last_seen.format_web(time_format) }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    </div>
                % else:
                    <div class="placeholder">
                        <h3>This bus doesn't have any recorded history</h3>
                        <p>There are a few reasons why that might be the case:</p>
                        <ol>
                            <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                            <li>It may not have been in service since BCTracker started recording bus history</li>
                            <li>It may not have functional tracking equipment installed</li>
                            % if model and model.type == ModelType.shuttle:
                                <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                            % end
                        </ol>
                        <p>Please check again later!</p>
                    </div>
                % end
            </div>
        </div>
    </div>
</div>
