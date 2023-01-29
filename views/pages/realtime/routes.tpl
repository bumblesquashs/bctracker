
% rebase('base', title='Realtime')

<div class="page-header">
    <h1 class="title">Realtime</h1>
    <h2 class="subtitle">Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'realtime') }}" class="tab-button">All Buses</a>
        <span class="tab-button current">By Route</span>
        <a href="{{ get_url(system, 'realtime/models') }}" class="tab-button">By Model</a>
        % if show_speed:
            <a href="{{ get_url(system, 'realtime/speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Dennis Hopper and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
    <hr />
</div>

% if len(positions) == 0:
    <div>
        % if system is not None and not system.realtime_enabled:
            <p>
                {{ system }} does not currently support realtime.
                You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
            </p>
        % else:
            % if system is None:
                There are no buses out right now.
                BC Transit does not have late night service, so this should be the case overnight.
                If you look out your window and the sun is shining, there may be an issue with the GTFS getting up-to-date info.
                Please check back later!
            % else:
                <p>
                    There are no buses out in {{ system }} right now.
                    Please choose a different system.
                </p>
            % end
        % end
    </div>
% elif system is None:
    <div>
        <p>
            Realtime routes can only be viewed for individual systems.
            Please choose a system.
        </p>
    </div>
% else:
    <div class="container">
        % for route in system.get_routes():
            % route_positions = [p for p in positions if p.trip is not None and p.trip.route == route]
            % if len(route_positions) == 0:
                % continue
            % end
            <div class="section">
                <div class="header">
                    <h2>{{ route.number }} {{! route.display_name }}</h2>
                </div>
                <div class="content">
                    <table class="striped">
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="desktop-only">Model</th>
                                % if system is None:
                                    <th class="non-mobile">System</th>
                                % end
                                <th class="desktop-only">Headsign</th>
                                <th class="desktop-only">Block</th>
                                <th class="desktop-only">Trip</th>
                                <th class="desktop-only">Next Stop</th>
                                <th class="non-desktop">Details</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_bus = None
                            % for position in sorted(route_positions):
                                % bus = position.bus
                                % order = bus.order
                                % if last_bus is None:
                                    % same_order = True
                                % elif order is None and last_bus.order is None:
                                    % same_order = True
                                % elif order is None or last_bus.order is None:
                                    % same_order = False
                                % else:
                                    % same_order = order == last_bus.order
                                % end
                                % last_bus = bus
                                <tr class="{{'' if same_order else 'divider'}}">
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
                                    % if system is None:
                                        <td class="non-mobile">{{ position.system }}</td>
                                    % end
                                    % trip = position.trip
                                    % block = position.trip.block
                                    % stop = position.stop
                                    <td>
                                        {{ trip }}
                                        % if stop is not None:
                                            <br class="non-desktop" />
                                            <span class="non-desktop smaller-font">
                                                % include('components/adherence_indicator', adherence=position.adherence)
                                                <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                            </span>
                                        % end
                                    </td>
                                    <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                    <td class="desktop-only"><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a></td>
                                    % if stop is None:
                                        <td class="desktop-only lighter-text">Unavailable</td>
                                    % else:
                                        <td class="desktop-only">
                                            % include('components/adherence_indicator', adherence=position.adherence)
                                            <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                        </td>
                                    % end
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
        
        % no_route_positions = sorted([p for p in positions if p.trip is None])
        % if len(no_route_positions) > 0:
            <div class="section">
                <div class="header">
                    <h2>Not In Service</h2>
                </div>
                <div class="content">
                    <table class="striped">
                        <thead>
                            <tr>
                                <th>Bus</th>
                                <th class="desktop-only">Model</th>
                                % if system is None:
                                    <th>System</th>
                                % end
                            </tr>
                        </thead>
                        <tbody>
                            % last_bus = None
                            % for position in no_route_positions:
                                % bus = position.bus
                                % order = bus.order
                                % if last_bus is None:
                                    % same_order = True
                                % elif order is None and last_bus.order is None:
                                    % same_order = True
                                % elif order is None or last_bus.order is None:
                                    % same_order = False
                                % else:
                                    % same_order = order == last_bus.order
                                % end
                                % last_bus = bus
                                <tr class="{{'' if same_order else 'divider'}}">
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
                                    % if system is None:
                                        <td>{{ position.system }}</td>
                                    % end
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            </div>
        % end
    </div>
% end

% include('components/top_button')
