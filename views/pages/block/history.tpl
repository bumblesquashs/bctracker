% from datetime import datetime

% from formatting import format_date, format_date_mobile

% rebase('base', title=f'Block {block.id} - History')

<div class="page-header">
    <h1 class="title">Block {{ block.id }} - History</h1>
    <a href="{{ get_url(system, f'block/{block.id}') }}">Return to block overview</a>
</div>
<hr />

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
                        {{ format_date(last_tracked) }}
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
                        {{ format_date(first_tracked) }}
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
        <p>This block doesn't have any recorded history.</p>
        <p>
            There are a few reasons why that might be the case:
            <ol>
                <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                <li>It may not have been in service since BCTracker started recording bus history</li>
                <li>It may not have functional NextRide equipment installed</li>
            </ol>
            Please check again later!
        </p>
    % else:
        <table class="pure-table pure-table-horizontal pure-table-striped">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Bus</th>
                    <th class="desktop-only">Model</th>
                    <th>First Seen</th>
                    <th>Last Seen</th>
                </tr>
            </thead>
            <tbody>
                % for record in records:
                    % bus = record.bus
                    % order = bus.order
                    <tr>
                        <td class="desktop-only">{{ format_date(record.date) }}</td>
                        <td class="non-desktop no-wrap">{{ format_date_mobile(record.date) }}</td>
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
                        <td class="desktop-only">{{ record.first_seen }}</td>
                        <td class="desktop-only">{{ record.last_seen }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
</div>

% include('components/top_button')
