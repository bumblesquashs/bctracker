
% rebase('base', title='Realtime')

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
    <div class="container no-inline">
        % models = sorted({p.bus.model for p in positions if p.bus.model is not None})
        
        % for model in models:
            % model_positions = sorted([p for p in positions if p.bus.model is not None and p.bus.model == model])
            % model_years = sorted({p.bus.order.year for p in model_positions})
            <div class="section">
                <h2 class="title">{{ model }}</h2>
                <table class="striped">
                    <thead>
                        <tr>
                            <th class="non-mobile">Number</th>
                            <th class="mobile-only">Bus</th>
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
                        % for year in model_years:
                            % year_positions = [p for p in model_positions if p.bus.order.year == year]
                            <tr class="section">
                                <td colspan="8">
                                    <div class="flex-row">
                                        <div class="flex-1">{{ year }}</div>
                                        <div>{{ len(year_positions) }}</div>
                                    </div>
                                </td>
                            </tr>
                            % for position in year_positions:
                                % include('components/realtime_row', position=position)
                            % end
                        % end
                    </tbody>
                </table>
            </div>
        % end
        
        % unknown_positions = sorted([p for p in positions if p.bus.order is None])
        % if len(unknown_positions) > 0:
            <div class="section">
                <h2 class="title">Unknown Year/Model</h2>
                <table class="striped">
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
                            % include('components/realtime_row', position=position)
                        % end
                    </tbody>
                </table>
            </div>
        % end
    </div>
% end

% include('components/top_button')
