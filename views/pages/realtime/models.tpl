
% rebase('base', title='Realtime', show_refresh_button=True)

<div class="page-header">
    <h1 class="title">Realtime</h1>
    <h2 class="subtitle">Currently active vehicles</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'realtime') }}" class="tab-button">All Buses</a>
        % if system is not None:
            <a href="{{ get_url(system, 'realtime/routes') }}" class="tab-button">By Route</a>
        % end
        <span class="tab-button current">By Model</span>
        % if show_speed:
            <a href="{{ get_url(system, 'realtime/speed') }}" class="tab-button">By Speed</a>
        % else:
            <!-- Oh, hello there! It's cool to see buses grouped in different ways, but I recently watched the movie Speed (1994) starring Keanu Reeves and now I want to see how fast these buses are going... if only there was a way to see realtime info by "speed"... -->
        % end
    </div>
    <hr />
</div>

% if len(positions) == 0:
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
    <div class="container no-inline">
        % models = sorted({p.bus.model for p in positions if p.bus.model is not None})
        
        % for model in models:
            % model_positions = sorted([p for p in positions if p.bus.model == model])
            <div class="section">
                <h2 class="title">{{ model }}</h2>
                <table class="striped fixed-table">
                    <thead>
                        <tr>
                            <th class="desktop-only">Number</th>
                            <th class="desktop-only">Year</th>
                            <th class="non-desktop" style="width: 20%;">Bus</th>
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
                        % last_year = None
                        % for position in model_positions:
                            % bus = position.bus
                            % order = bus.order
                            % same_year = last_year is None or order.year == last_year
                            % last_year = order.year
                            <tr class="{{'' if same_year else 'divider'}}">
                                <td>
                                    <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                    <br />
                                    <span class="non-desktop smaller-font">{{ order.year }}</span>
                                </td>
                                <td class="desktop-only">
                                    {{ order.year }}
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
                                            <br />
                                            <span class="non-desktop smaller-font">
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
            </div>
        % end
        
        % unknown_positions = sorted([p for p in positions if p.bus.order is None])
        % if len(unknown_positions) > 0:
            <div class="section">
                <h2 class="title">Unknown Model</h2>
                <table class="striped fixed-table">
                    <thead>
                        <tr>
                            <th class="desktop-only">Number</th>
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
                        % for position in unknown_positions:
                            <tr>
                                <td>{{ position.bus }}</td>
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
                                            <br />
                                            <span class="non-desktop smaller-font">
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
            </div>
        % end
    </div>
% end

% include('components/top_button')
