
% rebase('base', title=f'Trip {trip.id}', include_maps=True)

<div class="page-header">
    <h1 class="title">Trip {{! trip.display_id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">Overview</span>
        <a href="{{ get_url(system, f'trips/{trip.id}/map') }}" class="tab-button">Map</a>
        % if system.realtime_enabled:
            <a href="{{ get_url(system, f'trips/{trip.id}/history') }}" class="tab-button">History</a>
        % end
    </div>
    <hr />
</div>

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Overview</h2>
            </div>
            <div class="content">
                % include('components/map', map_trip=trip, map_positions=positions)
                
                <div class="info-box">
                    <div class="section no-flex">
                        % include('components/schedules_indicator', schedules=[trip.service.schedule])
                    </div>
                    <div class="section">
                        % route = trip.route
                        <div class="flex-row">
                            % include('components/route_indicator')
                            <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{! route.display_name }}</a>
                        </div>
                    </div>
                    <div class="section">
                        % block = trip.block
                        <div class="name">Block</div>
                        <div class="value">
                            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                        </div>
                    </div>
                    <div class="section">
                        <div class="name">Start time</div>
                        <div class="value">{{ trip.start_time.format_web(time_format) }}</div>
                    </div>
                    <div class="section">
                        <div class="name">End time</div>
                        <div class="value">{{ trip.end_time.format_web(time_format) }}</div>
                    </div>
                    <div class="section">
                        <div class="name">Duration</div>
                        <div class="value">{{ trip.duration }}</div>
                    </div>
                    <div class="section">
                        <div class="name">Number of stops</div>
                        <div class="value">{{ len(trip.departures) }}</div>
                    </div>
                    <div class="section">
                        <div class="name">Direction</div>
                        <div class="value">{{ trip.direction }}</div>
                    </div>
                </div>
            </div>
        </div>
        
        % related_trips = trip.related_trips
        % if len(related_trips) > 0:
            <div class="section">
                <div class="header">
                    <h2>Related Trips</h2>
                </div>
                <div class="content">
                    <table class="striped">
                        <thead>
                            <tr>
                                <th>Trip</th>
                                <th class="non-mobile">Block</th>
                                <th>Service Days</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for related_trip in related_trips:
                                % block = related_trip.block
                                <tr>
                                    <td><a href="{{ get_url(related_trip.system, f'trips/{related_trip.id}') }}">{{! related_trip.display_id }}</a></td>
                                    <td class="non-mobile"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                    <td>{{ related_trip.service }}</td>
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
                    <table class="striped">
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="non-mobile">Model</th>
                                <th>Next Stop</th>
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
                                        <div class="flex-column">
                                            <div class="flex-row left">
                                                <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                                % include('components/adherence_indicator', adherence=position.adherence)
                                            </div>
                                            <span class="mobile-only smaller-font">
                                                % if order is None:
                                                    <span class="lighter-text">Unknown Year/Model</span>
                                                % else:
                                                    {{! order }}
                                                % end
                                            </span>
                                        </div>
                                    </td>
                                    <td class="non-mobile">
                                        % if order is None:
                                            <span class="lighter-text">Unknown Year/Model</span>
                                        % else:
                                            {{! order }}
                                        % end
                                    </td>
                                    <td>
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
                <h2>Stop Schedule</h2>
            </div>
            <div class="content">
                % if len([d for d in trip.departures if d.timepoint]) > 0:
                    <p>
                        Departures in <span class="timing-point">bold</span> are timing points.
                    </p>
                % end
                <table class="striped">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th class="non-mobile">Stop Number</th>
                            <th class="non-mobile">Stop Name</th>
                            <th class="mobile-only">Stop</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for departure in trip.departures:
                            % stop = departure.stop
                            <tr>
                                <td class="{{ 'timing-point' if departure.timepoint else '' }}">
                                    {{ departure.time.format_web(time_format) }}
                                </td>
                                <td>
                                    <div class="flex-column">
                                        <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a>
                                        <span class="mobile-only smaller-font {{ 'timing-point' if departure.timepoint else '' }}">{{ stop }}</span>
                                    </div>
                                </td>
                                <td class="non-mobile">
                                    <div class="flex-column">
                                        <span class="{{ 'timing-point' if departure.timepoint else '' }}">
                                            {{ stop }}
                                        </span>
                                        % if not departure.pickup_type.is_normal:
                                            <span class="smaller-font">{{ departure.pickup_type }}</span>
                                        % elif departure == trip.last_departure:
                                            <span class="smaller-font">Drop off only</span>
                                        % end
                                        % if not departure.dropoff_type.is_normal:
                                            <span class="smaller-font">{{ departure.dropoff_type }}</span>
                                        % elif departure == trip.first_departure:
                                            <span class="smaller-font">Pick up only</span>
                                        % end
                                    </div>
                                </td>
                            </tr>
                        % end
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
