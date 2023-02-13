
% rebase('base', title='Realtime')

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
                                <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                % include('components/adherence_indicator', adherence=position.adherence)
                            </div>
                            <span class="non-desktop smaller-font">
                                % if order is None:
                                    <span class="lighter-text">Unknown Year/Model</span>
                                % else:
                                    {{! order }}
                                % end
                            </span>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % if order is None:
                            <span class="lighter-text">Unknown Year/Model</span>
                        % else:
                            {{! order }}
                        % end
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
                            </div>
                        </td>
                        <td class="non-mobile">
                            <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                        </td>
                        <td class="non-mobile">
                            <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{! trip.display_id }}</a>
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