
% from models.model import ModelType

% rebase('base')

<div id="page-header">
    <h1 class="row">
        <span>Bus</span>
        % include('components/bus', enable_link=False)
    </h1>
    % if bus.order is None:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % else:
        <h2>{{! bus.order }}</h2>
    % end
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'bus/{bus.number}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'bus/{bus.number}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
</div>

<div class="flex-container">
    % if overview is not None:
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header">
                    <h2>Overview</h2>
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section">
                            % include('components/events_list', events=events)
                        </div>
                        % record_systems = {r.system for r in records}
                        % if overview is not None:
                            % record_systems.add(overview.first_seen_system)
                            % record_systems.add(overview.last_seen_system)
                        % end
                        <div class="row section">
                            <div class="name">{{ 'System' if len(record_systems) == 1 else 'Systems' }}</div>
                            <div class="value">
                                % for record_system in sorted(record_systems):
                                    <a href="{{ get_url(record_system) }}">{{ record_system }}</a>
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
                    <div class="placeholder">
                        <h3>This bus doesn't have any recorded history</h3>
                        <p>There are a few reasons why that might be the case:</p>
                        <ol>
                            <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                            <li>It may not have been in service since BCTracker started recording bus history</li>
                            <li>It may not have functional NextRide equipment installed</li>
                            % model = bus.model
                            % if model is None or model.type == ModelType.shuttle:
                                <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                            % end
                        </ol>
                        <p>Please check again later!</p>
                    </div>
                % else:
                    % if len([r for r in records if len(r.warnings) > 0]) > 0:
                        <p>
                            <span>Entries with a</span>
                            <img class="middle-align white inline" src="/img/white/warning.png" />
                            <img class="middle-align black inline" src="/img/black/warning.png" />
                            <span>may be accidental logins.</span>
                        </p>
                    % end
                    <table>
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
                                        <div class="column">
                                            {{ record.date.format_short() }}
                                            <span class="smaller-font">{{ record.system }}</span>
                                        </div>
                                    </td>
                                    <td class="desktop-only">{{ record.system }}</td>
                                    <td>
                                        <div class="column">
                                            <div class="row">
                                                % if record.is_available:
                                                    % block = record.block
                                                    <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                                                % else:
                                                    <span>{{ record.block_id }}</span>
                                                % end
                                                % include('components/record_warnings')
                                            </div>
                                            <div class="non-desktop">
                                                % include('components/route_list', routes=record.routes)
                                            </div>
                                        </div>
                                    </td>
                                    <td class="desktop-only">
                                        % include('components/route_list', routes=record.routes)
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
