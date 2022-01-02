
% rebase('base', title='Realtime')

<div class="page-header">
    <h1 class="title">Realtime</h1>
    <h2 class="subtitle">Currently active vehicles</h2>
    % if group == 'all':
        <div class="tab-button-bar">
            <span class="tab-button current">All Buses</span>
            % if system is not None:
                <a href="?group=route" class="tab-button">By Route</a>
            % end
            <a href="?group=model" class="tab-button">By Model</a>
        </div>
    % elif group == 'route':
        <div class="tab-button-bar">
            <a href="?group=all" class="tab-button">All Buses</a>
            <span class="tab-button current">By Route</span>
            <a href="?group=model" class="tab-button">By Model</a>
        </div>
    % elif group == 'model':
        <div class="tab-button-bar">
            <a href="?group=all" class="tab-button">All Buses</a>
            % if system is not None:
                <a href="?group=route" class="tab-button">By Route</a>
            % end
            <span class="tab-button current">By Model</span>
        </div>
    % end
</div>
<hr />

<div class="container">
    % if len(buses) == 0:
        <div class="section">
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
        <div class="navigation"></div>
        
        % if group == 'all':
            <div class="section no-inline">
                % include('components/realtime_list', buses=buses)
            </div>
        % elif group == 'route':
            % if system is None:
                <div class="section no-inline">
                <p>
                    Realtime routes can only be viewed for individual systems.
                    Please choose a system.
                </p>
        
                % include('components/systems', realtime_only=True)
                </div>
            % else:
                % routes = sorted({b.position.trip.route for b in buses if b.position.trip is not None})
                
                % for route in routes:
                    % route_buses = [b for b in buses if b.position.trip is not None and b.position.trip.route == route]
                    <div class="section no-inline">
                        <h2 class="title">{{ route }}</h2>
                        % include('components/realtime_list', buses=route_buses)
                    </div>
                % end
                
                % no_route_buses = [b for b in buses if b.position.trip is None]
                    % if len(no_route_buses) > 0:
                    <div class="section no-inline">
                        <h2 class="title">Not In Service</h2>
                        % include('components/realtime_list', buses=no_route_buses)
                    </div>
                % end
            % end
        % elif group == 'model':
            % known_buses = [b for b in buses if b.order is not None]
            % models = sorted({b.model for b in known_buses})
            
            % for model in models:
                % model_buses = [b for b in known_buses if b.model == model]
                <div class="section no-inline">
                    <h2 class="title">{{ model }}</h2>
                    % include('components/realtime_list', buses=model_buses, show_model=False)
                </div>
            % end
            
            % unknown_buses = [b for b in buses if b.order is None]
            % if len(unknown_buses) > 0:
                <div class="section no-inline">
                    <h2 class="title">Unknown Model</h2>
                    % include('components/realtime_list', buses=unknown_buses, show_model=False)
                </div>
            % end
        % end
    % end
</div>

% include('components/top_button')
