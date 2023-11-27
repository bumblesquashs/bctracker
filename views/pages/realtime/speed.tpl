
% rebase('base')

<div class="page-header">
    <h1 class="title">Realtime</h1>
    <h2 class="subtitle">Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'realtime') }}" class="tab-button">All Buses</a>
        % if system is not None:
            <a href="{{ get_url(system, 'realtime/routes') }}" class="tab-button">By Route</a>
        % end
        <a href="{{ get_url(system, 'realtime/models') }}" class="tab-button">By Model</a>
        <span class="tab-button current">By Speed</span>
    </div>
</div>

% if len(positions) == 0:
    <div class="placeholder">
        % if system is None:
            <h3 class="title">There are no buses out right now</h3>
            <p>
                BC Transit does not have late night service, so this should be the case overnight.
                If you look out your window and the sun is shining, there may be an issue getting up-to-date info.
            </p>
            <p>Please check again later!</p>
        % elif not system.realtime_enabled:
            <h3 class="title">{{ system }} does not support realtime</h3>
            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % elif not system.is_loaded:
            <h3 class="title">Realtime information for {{ system }} is unavailable</h3>
            <p>System data is currently loading and will be available soon.</p>
        % else:
            <h3 class="title">There are no buses out in {{ system }} right now</h3>
            <p>Please check again later!</p>
        % end
    </div>
% else:
    <table class="striped">
        <thead>
            <tr>
                <th>Bus</th>
                <th class="desktop-only">Model</th>
                % if system is None:
                    <th class="desktop-only">System</th>
                % end
                <th class="desktop-only">Speed</th>
                <th>Headsign</th>
                <th class="non-mobile">Block</th>
                <th class="non-mobile">Trip</th>
                <th class="desktop-only">Next Stop</th>
            </tr>
        </thead>
        <tbody>
            % last_speed = None
            % for position in sorted(positions, key=lambda p: p.speed, reverse=True):
                % bus = position.bus
                % order = bus.order
                % same_speed = last_speed is None or position.speed // 10 == last_speed
                % last_speed = position.speed // 10
                <tr class="{{'' if same_speed else 'divider'}}">
                    <td>
                        <div class="flex-column">
                            <div class="flex-row left">
                                % include('components/bus', bus=bus)
                                % include('components/adherence_indicator', adherence=position.adherence)
                            </div>
                            <span class="non-desktop smaller-font">
                                % include('components/order', order=order)
                            </span>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % include('components/order', order=order)
                    </td>
                    % if system is None:
                        <td class="desktop-only">{{ position.system }}</td>
                    % end
                    <td class="desktop-only no-wrap">{{ position.speed }} km/h</td>
                    % if position.trip is None:
                        <td colspan="4">
                            <div class="flex-column">
                                <span class="lighter-text">Not in service</span>
                                <span class="non-desktop smaller-font no-wrap">{{ position.speed }} km/h</span>
                            </div>
                        </td>
                    % else:
                        % trip = position.trip
                        % block = trip.block
                        % stop = position.stop
                        <td>
                            <div class="flex-column">
                                % include('components/headsign_indicator')
                                <span class="non-desktop smaller-font no-wrap">{{ position.speed }} km/h</span>
                                <div class="mobile-only smaller-font">
                                    Trip: <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
                                </div>
                                % if stop is not None:
                                    <div class="non-desktop smaller-font">
                                        Next Stop: <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                                    </div>
                                % end
                            </div>
                        </td>
                        <td class="non-mobile">
                            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                        </td>
                        <td class="non-mobile">
                            <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.short_id }}</a>
                        </td>
                        <td class="desktop-only">
                            % if stop is None:
                                <span class="lighter-text">Unavailable</span>
                            % else:
                                <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop }}</a>
                            % end
                        </td>
                    % end
                </tr>
            % end
        </tbody>
    </table>
% end