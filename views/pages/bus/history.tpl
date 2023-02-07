
% from models.model import ModelType

% rebase('base', title=f'Bus {bus}')

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
    <hr />
</div>

<div class="flex-container">
    % if len(records) > 0:
        % last_tracked = records[0].date
        % days_since_last_tracked = last_tracked.format_since()
        
        % first_tracked = records[-1].date
        % days_since_first_tracked = first_tracked.format_since()
        
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header">
                    <h2>Overview</h2>
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section">
                            <div class="name">Last Tracked</div>
                            <div class="value">
                                % if days_since_last_tracked == '0 days ago':
                                    Today
                                % else:
                                    {{ last_tracked }}
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
                                    {{ first_tracked }}
                                    <br />
                                    <span class="smaller-font">{{ days_since_first_tracked }}</span>
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
                    % if len([r for r in records if r.is_suspicious]) > 0:
                        <p>
                            <span>Blocks with a</span>
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
                                        {{ record.date.format_short() }}
                                        <br />
                                        <span class="smaller-font">{{ record.system }}</span>
                                    </td>
                                    <td class="desktop-only">{{ record.system }}</td>
                                    <td>
                                        <div class="flex-row left">
                                            % if record.is_available:
                                                % block = record.block
                                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                            % else:
                                                <span>{{ record.block_id }}</span>
                                            % end
                                            % include('components/suspicious_record_indicator', record=record)
                                        </div>
                                        <div class="non-desktop">
                                            % include('components/route_indicator', routes=record.routes)
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/route_indicator', routes=record.routes)
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
