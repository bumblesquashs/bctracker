% from datetime import datetime
% import math

% from formatting import format_date, format_date_mobile
% from models.bus_model import BusModelType

% rebase('base', title=f'Bus {bus} History')

<div class="page-header">
    <h1 class="title">Bus {{ bus }} History</h1>
</div>
<hr />

% if len(history) > 0:
    % last_tracked = history[0].date
    % days_since_last_tracked = (datetime.now() - last_tracked).days
    
    % first_tracked = history[-1].date
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
                <div class="name">Days in Service</div>
                <div class="value">
                    % days_in_service = len({h.date.date() for h in history})
                    {{ days_in_service }}
                    <br />
                    <span class="smaller-font">
                        % total_days = math.floor((days_in_service / (last_tracked - first_tracked).days) * 100)
                        {{ total_days }}% in service rate
                    </span>
                </div>
            </div>
            <div class="section">
                % history_systems = sorted({h.system for h in history})
                <div class="name">System{{ '' if len(history_systems) == 1 else 's' }}</div>
                <div class="value">
                    % for history_system in history_systems:
                        <a href="{{ get_url(history_system) }}">{{ history_system }}</a>
                        <br />
                    % end
                </div>
            </div>
        </div>
    </div>
% end

<div>
    <h2>History</h2>
    % if len(history) == 0:
        <p>This bus doesn't have any recorded history.</p>
        <p>
            There are a few reasons why that might be the case:
            <ol>
                <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                <li>It may not have been in service since BCTracker started recording bus history</li>
                <li>It may not have functional NextRide equipment installed</li>
                % if model.type == BusModelType.shuttle:
                    <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                % end
            </ol>
            Please check again later!
        </p>
    % else:
        <table class="pure-table pure-table-horizontal pure-table-striped">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>System</th>
                    <th class="desktop-only">Assigned Block</th>
                    <th class="desktop-only">Assigned Routes</th>
                    <th class="desktop-only">Start Time</th>
                    <th class="desktop-only">End Time</th>
                    <th class="non-desktop">Block</th>
                    <th class="tablet-only">Time</th>
                </tr>
            </thead>
            <tbody>
                % for block_history in history:
                    <tr>
                        <td class="desktop-only">{{ format_date(block_history.date) }}</td>
                        <td class="non-desktop no-wrap">{{ format_date_mobile(block_history.date) }}</td>
                        <td>{{ block_history.system }}</td>
                        <td>
                            % if block_history.is_available:
                                % block = block_history.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % else:
                                <span>{{ block_history.block_id }}</span>
                            % end
                            <span class="non-desktop smaller-font">
                                <br />
                                {{ block_history.routes_string }}
                            </span>
                        </td>
                        <td class="desktop-only">{{ block_history.routes_string }}</td>
                        <td class="desktop-only">{{ block_history.start_time }}</td>
                        <td class="desktop-only">{{ block_history.end_time }}</td>
                        <td class="tablet-only">{{ block_history.start_time }} - {{ block_history.end_time }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
</div>
