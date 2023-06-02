
% rebase('base')

<div class="page-header">
    <h1 class="title">Trip {{! trip.display_id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'trips/{trip.id}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'trips/{trip.id}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
</div>

% if system.realtime_enabled:
    <div class="flex-container">
        % if len(records) > 0:
            <div class="sidebar container flex-1">
                <div class="section">
                    <div class="header">
                        <h2>Overview</h2>
                    </div>
                    <div class="content">
                        <div class="info-box">
                            <div class="section no-flex">
                                % include('components/events_indicator', events=events)
                            </div>
                            <div class="section">
                                % orders = sorted({r.bus.order for r in records if r.bus.order is not None})
                                <div class="name">{{ 'Model' if len(orders) == 1 else 'Models' }}</div>
                                <div class="value flex-column">
                                    % for order in orders:
                                        <div>{{! order }}</div>
                                    % end
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        % end
        
        <div class="container flex-3">
            <div class="section">
                <div class="header">
                    <h2>History</h2>
                </div>
                <div class="content">
                    % if len(records) == 0:
                        <p>This trip doesn't have any recorded history.</p>
                        <p>
                            There are a few reasons why that might be the case:
                            <ol>
                                <li>It may be a new trip introduced in the last service change</li>
                                <li>It may not be operating due to driver or vehicle shortages</li>
                                <li>It may have only been done by buses without functional NextRide equipment installed</li>
                            </ol>
                            Please check again later!
                        </p>
                    % else:
                        % if len([r for r in records if len(r.warnings) > 0]) > 0:
                            <p>
                                <span>Entries with a</span>
                                <img class="middle-align white inline" src="/img/white/warning.png" />
                                <img class="middle-align black inline" src="/img/black/warning.png" />
                                <span>may be accidental logins.</span>
                            </p>
                        % end
                        <table class="striped">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Bus</th>
                                    <th class="desktop-only">Model</th>
                                    <th class="non-mobile">First Seen</th>
                                    <th>Last Seen</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for record in records:
                                    % bus = record.bus
                                    % order = bus.order
                                    <tr>
                                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                                        <td class="non-desktop">{{ record.date.format_short() }}</td>
                                        <td>
                                            <div class="flex-column">
                                                <div class="flex-row left">
                                                    % include('components/bus', bus=bus)
                                                    % include('components/record_warnings_indicator', record=record)
                                                </div>
                                                <span class="non-desktop smaller-font">
                                                    % include('components/order', order=order)
                                                </span>
                                            </div>
                                        </td>
                                        <td class="desktop-only">
                                            % include('components/order', order=order)
                                        </td>
                                        <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                        <td>{{ record.last_seen.format_web(time_format) }}</td>
                                    </tr>
                                % end
                            </tbody>
                        </table>
                    % end
                </div>
            </div>
        </div>
    </div>
    
    % include('components/top_button')
% else:
    <p>
        {{ system }} does not currently support realtime.
        You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
    </p>
% end
