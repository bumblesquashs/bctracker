% from datetime import datetime

% import formatting

% rebase('base', title=f'Trip {trip.id}')

<div class="page-header">
    <h1 class="title">Trip {{ trip.id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'trips/{trip.id}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'trips/{trip.id}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
</div>
<hr />

% if system.realtime_enabled:
    % if len(records) > 0:
        % last_tracked = records[0].date
        % days_since_last_tracked = (datetime.now() - last_tracked).days
        
        % first_tracked = records[-1].date
        % days_since_first_tracked = (datetime.now() - first_tracked).days
        
        <div id="sidebar">
            <h2>Overview</h2>
            <div class="info-box">
                <div class="section">
                    <div class="name">Last Tracked</div>
                    <div class="value">
                        % if days_since_last_tracked == 0:
                            Today
                        % else:
                            {{ formatting.short(last_tracked) }}
                            <br />
                            <span class="smaller-font">
                                % if days_since_last_tracked == 1:
                                    1 day ago
                                % else:
                                    {{ days_since_last_tracked }} days ago
                                % end
                            </span>
                        % end
                    </div>
                </div>
                <div class="section">
                    <div class="name">First Tracked</div>
                    <div class="value">
                        % if days_since_first_tracked == 0:
                            Today
                        % else:
                            {{ formatting.short(first_tracked) }}
                            <br />
                            <span class="smaller-font">
                                % if days_since_first_tracked == 1:
                                    1 day ago
                                % else:
                                    {{ days_since_first_tracked }} days ago
                                % end
                            </span>
                        % end
                    </div>
                </div>
                <div class="section">
                    % orders = sorted({r.bus.order for r in records if r.bus.order is not None})
                    <div class="name">Model{{ '' if len(orders) == 1 else 's' }}</div>
                    <div class="value">
                        % for order in orders:
                            <span>{{ order }}</span>
                            <br />
                        % end
                    </div>
                </div>
            </div>
        </div>
    % end
    
    <div>
        <h2>History</h2>
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
            <table class="striped">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Bus</th>
                        <th class="desktop-only">Model</th>
                        <th class="non-mobile">First Seen</th>
                        <th class="non-mobile">Last Seen</th>
                    </tr>
                </thead>
                <tbody>
                    % for record in records:
                        % bus = record.bus
                        % order = bus.order
                        <tr>
                            <td class="desktop-only">{{ formatting.long(record.date) }}</td>
                            <td class="non-desktop no-wrap">{{ formatting.short(record.date) }}</td>
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
                            <td class="non-mobile">{{ record.first_seen }}</td>
                            <td class="non-mobile">{{ record.last_seen }}</td>
                        </tr>
                    % end
                </tbody>
            </table>
        % end
    </div>
    
    % include('components/top_button')
% else:
    <p>
        {{ system }} does not currently support realtime.
        You can browse the schedule data for {{ system }} using the links above, or choose another system that supports realtime from the following list.
    </p>

    % include('components/systems', realtime_only=True)
% end
