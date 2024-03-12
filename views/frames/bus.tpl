
% from datetime import timedelta

% from models.date import Date

% model = bus.model

<a href="{{ get_url(system, f'bus/{bus.number}') }}">See all details</a>

<div class="sidebar container">
    <div class="section">
        <div class="header">
            <h2>Realtime Information</h2>
        </div>
        <div class="content">
            % if position.trip is None:
                <div class="info-box">
                    <div class="section">
                        <h3>Not in service</h3>
                    </div>
                    % last_record = overview.last_record
                    % if last_record is not None and last_record.date.is_today:
                        % block = last_record.block
                        % if block is not None:
                            % date = Date.today(block.system.timezone)
                            % end_time = block.get_end_time(date=date)
                            % if end_time is not None and end_time.is_later:
                                <div class="section no-flex">
                                    % include('components/block_timeline', date=date)
                                </div>
                            % end
                        % end
                    % end
                    <div class="row section">
                        <div class="name">System</div>
                        <div class="value">
                            <a href="{{ get_url(position.system) }}">{{ position.system }}</a>
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
                % block = trip.block
                % route = trip.route
                
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
                            <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                        </div>
                    </div>
                    <div class="section">
                        % include('components/block_timeline', date=Date.today(block.system.timezone))
                    </div>
                    <div class="row section">
                        <div class="name">System</div>
                        <div class="value">
                            <a href="{{ get_url(trip.system) }}">{{ trip.system }}</a>
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
                            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
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
                </div>
            % end
        </div>
    </div>
    
    % upcoming_departures = position.find_upcoming_departures()
    % if len(upcoming_departures) > 0:
        <div class="section">
            <div class="header">
                <h2>Upcoming Stops</h2>
            </div>
            <div class="content">
                % if len([d for d in upcoming_departures if d.timepoint]) > 0:
                    <p>Departures in <span class="timing-point">bold</span> are timing points.</p>
                % end
                % if position.adherence is not None and position.adherence.value != 0:
                    <p>Times in brackets are estimates based on current location.</p>
                % end
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th class="non-mobile">Stop Number</th>
                            <th class="non-mobile">Stop Name</th>
                            <th class="mobile-only">Stop</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for departure in upcoming_departures:
                            % trip = departure.trip
                            % stop = departure.stop
                            <tr>
                                <td>
                                    <div class="column">
                                        <div class="{{ 'timing-point' if departure.timepoint else '' }}">
                                            {{ departure.time.format_web(time_format) }}
                                        </div>
                                        % if position.adherence is not None and position.adherence.value != 0:
                                            % expected_time = departure.time - timedelta(minutes=position.adherence.value)
                                            <div class="smaller-font lighter-text">
                                                ({{ expected_time.format_web(time_format) }})
                                            </div>
                                        % end
                                    </div>
                                </td>
                                % if stop is None:
                                    <td class="lighter-text" colspan="2">Unknown</td>
                                % else:
                                    <td>
                                        <div class="column">
                                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a>
                                            <div class="mobile-only smaller-font {{ 'timing-point' if departure.timepoint else '' }}">{{ stop }}</div>
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        <div class="column">
                                            <div class="{{ 'timing-point' if departure.timepoint else '' }}">{{ stop }}</div>
                                            % if not departure.pickup_type.is_normal:
                                                <span class="smaller-font">{{ departure.pickup_type }}</span>
                                            % elif departure == trip.last_departure:
                                                <span class="smaller-font">No pick up</span>
                                            % end
                                            % if not departure.dropoff_type.is_normal:
                                                <span class="smaller-font">{{ departure.dropoff_type }}</span>
                                            % elif departure == trip.first_departure:
                                                <span class="smaller-font">No drop off</span>
                                            % end
                                        </div>
                                    </td>
                                % end
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        </div>
    % end
</div>
