
% from models.model import ModelType

% rebase('base')

<div class="page-header">
    <h1 class="title">Bus {{ bus }}</h1>
    <h2 class="subtitle">
        % if bus.order is None:
            <span class="lighter-text">Unknown Year/Model</span>
        % else:
            {{! bus.order }}
        % end
    </h2>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'bus/{bus.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
</div>

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Overview</h2>
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="section">
                        <div class="name">Last Seen</div>
                        <div class="value flex-column">
                            % if overview is None:
                                <div class="lighter-text">Never</div>
                            % else:
                                % last_seen = overview.last_seen_date
                                % if last_seen.is_today:
                                    Today
                                % else:
                                    {{ last_seen }}
                                    <span class="smaller-font">{{ last_seen.format_since() }}</span>
                                % end
                            % end
                        </div>
                    </div>
                    % if overview is not None:
                        % last_record = overview.last_record
                        % if last_record is not None:
                            <div class="section">
                                <div class="name">Last Tracked</div>
                                <div class="value flex-column">
                                    % last_tracked = last_record.date
                                    % if last_tracked.is_today:
                                        Today
                                    % else:
                                        {{ last_tracked }}
                                        <span class="smaller-font">{{ last_tracked.format_since() }}</span>
                                    % end
                                </div>
                            </div>
                        % end
                        <div class="section">
                            <div class="name">First Seen</div>
                            <div class="value flex-column">
                                % first_seen = overview.first_seen_date
                                % if first_seen.is_today:
                                    Today
                                % else:
                                    {{ first_seen }}
                                    <span class="smaller-font">{{ first_seen.format_since() }}</span>
                                % end
                            </div>
                        </div>
                        % first_record = overview.first_record
                        % if first_record is not None:
                            <div class="section">
                                <div class="name">First Tracked</div>
                                <div class="value flex-column">
                                    % first_tracked = first_record.date
                                    % if first_tracked.is_today:
                                        Today
                                    % else:
                                        {{ first_tracked }}
                                        <span class="smaller-font">{{ first_tracked.format_since() }}</span>
                                    % end
                                </div>
                            </div>
                        % end
                    % end
                    % record_systems = {r.system for r in records}
                    % if overview is not None:
                        % record_systems.add(overview.first_seen_system)
                        % record_systems.add(overview.last_seen_system)
                    % end
                    % if len(record_systems) > 0:
                        <div class="section">
                            <div class="name">{{ 'System' if len(record_systems) == 1 else 'Systems' }}</div>
                            <div class="value flex-column">
                                % for record_system in sorted(record_systems):
                                    <a href="{{ get_url(record_system) }}">{{ record_system }}</a>
                                % end
                            </div>
                        </div>
                    % end
                </div>
            </div>
        </div>
    </div>
    
    <div class="container flex-3">
        <div class="section">
            <div class="header">
                <h2>History</h2>
            </div>
            <div class="content">
                % if len(records) == 0:
                    <p>This bus doesn't have any recorded history.</p>
                    <p>
                        There are a few reasons why that might be the case:
                        <ol>
                            <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                            <li>It may not have been in service since BCTracker started recording bus history</li>
                            <li>It may not have functional NextRide equipment installed</li>
                            % model = bus.model
                            % if model is None or model.type == ModelType.shuttle:
                                <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                            % end
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
                                <th class="desktop-only">System</th>
                                <th>Block</th>
                                <th class="desktop-only">Routes</th>
                                <th class="desktop-only">Start Time</th>
                                <th class="desktop-only">End Time</th>
                                <th class="non-mobile">First Seen</th>
                                <th class="no-wrap">Last Seen</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for record in records:
                                <tr>
                                    <td class="desktop-only">{{ record.date.format_long() }}</td>
                                    <td class="non-desktop">
                                        <div class="flex-column">
                                            {{ record.date.format_short() }}
                                            <span class="smaller-font">{{ record.system }}</span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">{{ record.system }}</td>
                                    <td>
                                        <div class="flex-column">
                                            <div class="flex-row left">
                                                % if record.is_available:
                                                    % block = record.block
                                                    <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                                % else:
                                                    <span>{{ record.block_id }}</span>
                                                % end
                                                % include('components/record_warnings_indicator', record=record)
                                            </div>
                                            <div class="non-desktop">
                                                % include('components/routes_indicator', routes=record.routes)
                                            </div>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/routes_indicator', routes=record.routes)
                                    </td>
                                    <td class="desktop-only">{{ record.start_time.format_web(time_format) }}</td>
                                    <td class="desktop-only">{{ record.end_time.format_web(time_format) }}</td>
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
