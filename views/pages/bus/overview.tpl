
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
    % if bus.order:
        <h2>{{! bus.order }}</h2>
    % else:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % end
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, 'bus', bus, 'map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, 'bus', bus, 'history') }}" class="tab-button">History</a>
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
                % if not position:
                    <div class="info-box">
                        <div class="section">
                            <h3>Not in service</h3>
                        </div>
                        <div class="row section">
                            <div class="name">Last Seen</div>
                            <div class="value">
                                % if overview:
                                    % last_seen = overview.last_seen_date
                                    % if last_seen.is_today:
                                        <div>Today</div>
                                    % else:
                                        <div>{{ last_seen.format_long() }}</div>
                                        <div class="smaller-font">{{ last_seen.format_since() }}</div>
                                    % end
                                % else:
                                    <div class="lighter-text">Never</div>
                                % end
                            </div>
                        </div>
                        % if overview:
                            <div class="row section">
                                <div class="name">System</div>
                                <div class="value">
                                    <a href="{{ get_url(overview.last_seen_system) }}">{{ overview.last_seen_system }}</a>
                                </div>
                            </div>
                        % end
                    </div>
                % elif not position.trip:
                    % include('components/map', map_position=position)
                    
                    <div class="info-box">
                        <div class="section">
                            <h3>Not in service</h3>
                        </div>
                        % last_record = overview.last_record
                        % if last_record and last_record.date.is_today:
                            % block = last_record.block
                            % if block:
                                % date = Date.today(block.system.timezone)
                                % end_time = block.get_end_time(date=date)
                                % if end_time and end_time.is_later:
                                    <div class="section no-flex">
                                        % include('components/block_timeline', date=date)
                                    </div>
                                % end
                            % end
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
                                <a href="{{ get_url(position.system) }}">{{ position.system }}</a>
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
                    </div>
                % else:
                    % trip = position.trip
                    % stop = position.stop
                    % block = trip.block
                    % route = trip.route
                    
                    % include('components/map', map_position=position, map_trip=trip, map_departures=trip.find_departures(), zoom_trips=False, zoom_departures=False)
                    
                    <div class="info-box">
                        <div class="section">
                            <div class="row">
                                % include('components/adherence', adherence=position.adherence, size='large')
                                <h3>{{ trip }}</h3>
                            </div>
                        </div>
                        <div class="section">
                            <div class="row">
                                % include('components/route')
                                <a href="{{ get_url(route.system, 'routes', route) }}">{{! route.display_name }}</a>
                            </div>
                        </div>
                        <div class="section">
                            % include('components/block_timeline', date=Date.today(block.system.timezone))
                        </div>
                        % if position.timestamp:
                            <div class="row section">
                                <div class="name">Last Update</div>
                                <div class="value">
                                    <div id="timestamp"></div>
                                    <script>
                                        updateTimestampFunctions.push(function(currentTime) {
                                            const difference = getDifference(currentTime, originalTimestamp + timestampOffset);
                                            document.getElementById("timestamp").innerHTML = difference;
                                        });
                                    </script>
                                </div>
                            </div>
                        % end
                        <div class="row section">
                            <div class="name">System</div>
                            <div class="value">
                                <a href="{{ get_url(trip.system) }}">{{ trip.system }}</a>
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
                        <div class="row section">
                            <div class="name">Block</div>
                            <div class="value">
                                <a href="{{ get_url(block.system, 'blocks', block) }}">{{ block.id }}</a>
                                % date = Date.today(block.system.timezone)
                                % start_time = block.get_start_time(date=date).format_web(time_format)
                                % end_time = block.get_end_time(date=date).format_web(time_format)
                                % duration = block.get_duration(date=date)
                                <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ duration }})</span>
                            </div>
                        </div>
                        <div class="row section">
                            <div class="name">Trip</div>
                            <div class="value">
                                % include('components/trip')
                                % start_time = trip.start_time.format_web(time_format)
                                % end_time = trip.end_time.format_web(time_format)
                                <span class="smaller-font">{{ start_time }} - {{ end_time }} ({{ trip.duration }})</span>
                            </div>
                        </div>
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
                    </div>
                % end
            </div>
        </div>
        
        % if bus.order:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Details</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="info-box">
                        % if bus.order.size > 1:
                            <div class="section">
                                % include('components/order_details')
                            </div>
                        % end
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
                    </div>
                </div>
            </div>
        % end
    </div>
    
    <div class="container flex-3">
        % if position:
            % upcoming_departures = position.find_upcoming_departures()
            % if upcoming_departures:
                <div class="section">
                    <div class="header" onclick="toggleSection(this)">
                        <h2>Upcoming Stops</h2>
                        % include('components/toggle')
                    </div>
                    <div class="content">
                        % if [d for d in upcoming_departures if d.timepoint]:
                            <p>Departures in <span class="timing-point">bold</span> are timing points.</p>
                        % end
                        % if position.adherence and position.adherence.value != 0:
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
                                                % include('components/svg', name='down')
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
        % end
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Recent History</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if records:
                    % if [r for r in records if r.warnings]:
                        <p>
                            <span>Entries with a</span>
                            <span class="record-warnings">
                                % include('components/svg', name='warning')
                            </span>
                            <span>may be accidental logins.</span>
                        </p>
                    % end
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th class="desktop-only">System</th>
                                <th>Block</th>
                                <th class="desktop-only">Routes</th>
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
                                            <span class="non-desktop smaller-font">{{ record.system }}</span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">{{ record.system }}</td>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % if record.is_available:
                                                    % block = record.block
                                                    <a href="{{ get_url(block.system, 'blocks', block) }}">{{ block.id }}</a>
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
                                    <td class="desktop-only">{{ record.start_time.format_web(time_format) }}</td>
                                    <td class="desktop-only">{{ record.end_time.format_web(time_format) }}</td>
                                    <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                    <td>{{ record.last_seen.format_web(time_format) }}</td>
                                </tr>
                            % end
                        </tbody>
                    </table>
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
