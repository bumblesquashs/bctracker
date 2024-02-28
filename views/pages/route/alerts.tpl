
% rebase('base')

<div id="page-header">
    <h1 class="row">
        % include('components/route')
        {{! route.display_name }}
    </h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'routes/{route.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'routes/{route.number}/map') }}" class="tab-button">Map</a>
        <a href="{{ get_url(system, f'routes/{route.number}/schedule') }}" class="tab-button">Schedule</a>
        <span class="tab-button current">Alerts</a>
    </div>
</div>

% if len(alerts) == 0:
    <div class="placeholder">
        <h2>No Alerts</h2>
    </div>
% else:
    <div class="container">
        % for alert in alerts:
            <div class="section">
                <div class="header">
                    <h2>{{ alert }}</h2>
                    % if alert.active_periods:
                        <b>{{ alert.active_periods }}</b>
                    % end
                </div>
                <div class="content">
                    % if alert.description:
                        {{ alert.description }}
                    % end
                    % alert_targets = [t for t in targets if t.alert_id == alert.id]
                    <div class="column">
                        % for target in alert_targets:
                            % stop = target.stop
                            % trip = target.trip
                            % if stop:
                                <div class="row">
                                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">{{ stop.number }}</a>
                                    {{ stop }}
                                </div>
                            % end
                            % if trip:
                                <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip }}</a>
                            % end
                        % end
                    </div>
                </div>
            </div>
        % end
    </div>
% end
