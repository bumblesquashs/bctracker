
% rebase('base', title='Realtime')

<div class="page-header">
    <h1 class="title">Realtime</h1>
    <h2 class="subtitle">Currently active vehicles</h2>
    <div class="tab-button-bar">
        <span class="tab-button current">All Buses</span>
        % if system is not None:
            <a href="{{ get_url(system, 'realtime/routes') }}" class="tab-button">By Route</a>
        % end
        <a href="{{ get_url(system, 'realtime/models') }}" class="tab-button">By Model</a>
        % if show_speed:
            <a href="{{ get_url(system, 'realtime/speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Keanu Reeves and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
</div>
<hr />

% if len(buses) == 0:
    <div>
        % if system is not None and not system.realtime_enabled:
            <p>
                {{ system }} does not currently support realtime.
                You can browse the schedule data for {{ system }} using the links above, or choose another system that supports realtime from the following list.
            </p>
            
            % include('components/systems', realtime_only=True)
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
                
                % include('components/systems', realtime_only=True)
            % end
        % end
    </div>
% else:
    <table class="striped fixed-table">
        <thead>
            <tr>
                <th class="desktop-only">Number</th>
                <th class="desktop-only">Model</th>
                <th class="non-desktop">Bus</th>
                % if system is None:
                    <th class="non-mobile">System</th>
                % end
                <th class="desktop-only">Headsign</th>
                <th class="desktop-only">Current Block</th>
                <th class="desktop-only">Current Trip</th>
                <th class="desktop-only">Current Stop</th>
                <th class="non-desktop">Details</th>
            </tr>
        </thead>
        <tbody>
            % last_order = None
            % for bus in sorted(buses):
                % position = bus.position
                % order = bus.order
                % same_order = last_order is None or order == last_order
                % last_order = order
                <tr class="{{'' if same_order else 'divider'}}">
                    <td>
                        % if bus.is_unknown:
                            {{ bus }}
                        % else:
                            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                        % end
                        % if order is not None:
                            <span class="non-desktop smaller-font">
                                <br />
                                {{ order }}
                            </span>
                        % end
                    </td>
                    <td class="desktop-only">
                        % if order is not None:
                            {{ order }}
                        % end
                    </td>
                    % if system is None:
                        <td class="non-mobile">{{ position.system }}</td>
                    % end
                    % if position.trip is None:
                        <td class="lighter-text">Not in service</td>
                        <td class="desktop-only"></td>
                        <td class="desktop-only"></td>
                        <td class="desktop-only"></td>
                    % else:
                        % trip = position.trip
                        % block = position.trip.block
                        % stop = position.stop
                        <td>
                            {{ trip }}
                            % if stop is not None:
                                <span class="non-desktop smaller-font">
                                    <br />
                                    % include('components/adherence_indicator', adherence=position.schedule_adherence)
                                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                </span>
                            % end
                        </td>
                        <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                        <td class="desktop-only"><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
                        % if stop is None:
                            <td class="desktop-only lighter-text">Unavailable</td>
                        % else:
                            <td class="desktop-only">
                                % include('components/adherence_indicator', adherence=position.schedule_adherence)
                                <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                            </td>
                        % end
                    % end
                </tr>
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
