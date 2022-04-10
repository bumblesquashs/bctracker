
% import formatting

% rebase('base', title=f'Trip {trip.id}', show_refresh_button=True)

<div class="page-header">
    <h1 class="title trip-id">Trip {{ trip.id }}</h1>
    <h2 class="subtitle">{{ trip }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'trips/{trip.id}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'trips/{trip.id}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
    <hr />
</div>

% if system.realtime_enabled:
    % if len(records) > 0:
        % last_tracked = records[0].date
        % days_since_last_tracked = formatting.days_since(last_tracked)
        
        % first_tracked = records[-1].date
        % days_since_first_tracked = formatting.days_since(first_tracked)
        
        <div class="sidebar">
            <h2>Overview</h2>
            <div class="info-box">
                <div class="section">
                    <div class="name">Last Tracked</div>
                    <div class="value">
                        % if days_since_last_tracked == '0 days ago':
                            Today
                        % else:
                            {{ formatting.short(last_tracked) }}
                            <br />
                            <span class="smaller-font">{{ days_since_last_tracked }}</span>
                        % end
                    </div>
                </div>
                <div class="section">
                    <div class="name">First Tracked</div>
                    <div class="value">
                        % if days_since_first_tracked == '0 days ago':
                            Today
                        % else:
                            {{ formatting.short(first_tracked) }}
                            <br />
                            <span class="smaller-font">{{ days_since_first_tracked }}</span>
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
                        <th>Last Seen</th>
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
                                % if order is None:
                                    {{ bus }}
                                % else:
                                    <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                    <br />
                                    <span class="non-desktop smaller-font">{{ order }}</span>
                                % end
                            </td>
                            <td class="desktop-only">
                                % if order is not None:
                                    {{ order }}
                                % end
                            </td>
                            <td class="non-mobile">{{ record.first_seen }}</td>
                            <td>{{ record.last_seen }}</td>
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
