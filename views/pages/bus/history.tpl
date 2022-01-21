% from datetime import datetime
% import math

% from formatting import format_date, format_date_mobile
% from models.model import BusModelType

% rebase('base', title=f'Bus {bus}')

<div class="page-header">
    <h1 class="title">Bus {{ bus }}</h1>
    <h2 class="subtitle">{{ bus.order }}</h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'bus/{bus.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
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
                % record_systems = sorted({r.system for r in records})
                <div class="name">System{{ '' if len(record_systems) == 1 else 's' }}</div>
                <div class="value">
                    % for record_system in record_systems:
                        <a href="{{ get_url(record_system) }}">{{ record_system }}</a>
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
        <p>This bus doesn't have any recorded history.</p>
        <p>
            There are a few reasons why that might be the case:
            <ol>
                <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                <li>It may not have been in service since BCTracker started recording bus history</li>
                <li>It may not have functional NextRide equipment installed</li>
                % model = bus.model
                % if model is not None and model.type == BusModelType.shuttle:
                    <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                % end
            </ol>
            Please check again later!
        </p>
    % else:
        <table class="striped">
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
                    <th class="desktop-only">First Seen</th>
                    <th class="desktop-only">Last Seen</th>
                </tr>
            </thead>
            <tbody>
                % for record in records:
                    <tr>
                        <td class="desktop-only">{{ format_date(record.date) }}</td>
                        <td class="non-desktop no-wrap">{{ format_date_mobile(record.date) }}</td>
                        <td>{{ record.system }}</td>
                        <td>
                            % if record.is_available:
                                % block = record.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % else:
                                <span>{{ record.block_id }}</span>
                            % end
                            <span class="non-desktop smaller-font">
                                <br />
                                {{ record.routes }}
                            </span>
                        </td>
                        <td class="desktop-only">{{ record.routes }}</td>
                        <td class="desktop-only">{{ record.start_time }}</td>
                        <td class="desktop-only">{{ record.end_time }}</td>
                        <td class="tablet-only">{{ record.start_time }} - {{ record.end_time }}</td>
                        <td class="desktop-only">{{ record.first_seen }}</td>
                        <td class="desktop-only">{{ record.last_seen }}</td>
                    </tr>
                % end
            </tbody>
        </table>
    % end
</div>

% include('components/top_button')
