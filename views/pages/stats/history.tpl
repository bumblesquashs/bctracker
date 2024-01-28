
% from datetime import timedelta

% from models.date import Date

% if system is None:
    % today = Date.today()
% else:
    % today = Date.today(system.timezone)
% end

% rebase('base')

<div id="page-header">
    <h1>Statistics</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'stats') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, 'stats/realtime') }}" class="tab-button">Realtime</a>
        <span class="tab-button current">History</span>
    </div>
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Transfers</h2>
            </div>
            <div class="content">
                % if len(transfers) == 0:
                    <div class="placeholder">
                        % if system is None:
                            <h3>No transfers found</h3>
                            <p>Something has probably gone terribly wrong if you're seeing this.</p>
                        % elif not system.realtime_enabled:
                            <h3>{{ system }} does not currently support realtime</h3>
                            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
                        % else:
                            <h3>No buses have been transferred to or from {{ system }}</h3>
                            <p>Please check again later!</p>
                        % end
                    </div>
                % else:
                    % if system is None:
                        <table>
                            <thead>
                                <tr>
                                    <th>System</th>
                                    <th>Gained</th>
                                    <th>Lost</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for region in regions:
                                    <tr class="header">
                                        <td colspan="3">{{ region }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % region_systems = [s for s in systems if s.region == region]
                                    % for region_system in region_systems:
                                        <tr>
                                            <td><a href="{{ get_url(region_system, path) }}">{{ region_system }}</a></td>
                                            <td>{{ len([t for t in transfers if t.new_system == region_system]) }}</td>
                                            <td>{{ len([t for t in transfers if t.old_system == region_system]) }}</td>
                                        </tr>
                                    % end
                                % end
                            </tbody>
                        </table>
                    % else:
                        % models = sorted({t.bus.model for t in transfers if t.bus.model is not None})
                        % model_types = sorted({m.type for m in models})
                        
                        <table>
                            <thead>
                                <tr>
                                    <th>Model</th>
                                    <th>Gained</th>
                                    <th>Lost</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for type in model_types:
                                    % type_transfers = [t for t in transfers if t.bus.model is not None and t.bus.model.type == type]
                                    <tr class="header">
                                        <td>{{ type }}</td>
                                        <td>{{ len([t for t in type_transfers if t.new_system == system]) }}</td>
                                        <td>{{ len([t for t in type_transfers if t.old_system == system]) }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % type_models = [m for m in models if m.type == type]
                                    % for model in type_models:
                                        % model_transfers = [t for t in type_transfers if t.bus.model == model]
                                        <tr>
                                            <td><a href="{{ get_url(system, f'fleet#{model.id}') }}">{{! model }}</a></td>
                                            <td>{{ len([t for t in model_transfers if t.new_system == system]) }}</td>
                                            <td>{{ len([t for t in model_transfers if t.old_system == system]) }}</td>
                                        </tr>
                                    % end
                                % end
                                <tr class="header">
                                    <td>Total</td>
                                    <td>{{ len([t for t in transfers if t.new_system == system]) }}</td>
                                    <td>{{ len([t for t in transfers if t.old_system == system]) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    % end
                % end
            </div>
        </div>
    </div>
    <div class="inline container flex-3">
        <div class="section">
            <div class="header">
                <h2>Today</h2>
            </div>
            <div class="content">
                % today_overviews = [o for o in overviews if o.last_seen_date >= today]
                % if len(today_overviews) == 0:
                    <div class="placeholder">
                        <h3>No buses seen today</h3>
                    </div>
                % else:
                    % if system is None:
                        <table>
                            <thead>
                                <tr>
                                    <th>System</th>
                                    <th>Seen</th>
                                    <th>Tracked</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for region in regions:
                                    <tr class="header">
                                        <td colspan="3">{{ region }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % region_systems = [s for s in systems if s.region == region]
                                    % for region_system in region_systems:
                                        % region_system_overviews = [o for o in today_overviews if o.last_seen_system == region_system]
                                        <tr>
                                            <td><a href="{{ get_url(region_system, path) }}">{{ region_system }}</a></td>
                                            <td>{{ len(region_system_overviews) }}</td>
                                            <td>{{ len([o for o in region_system_overviews if o.last_record is not None and o.last_record.system == region_system and o.last_record.date == today]) }}</td>
                                        </tr>
                                    % end
                                % end
                                <tr class="header">
                                    <td>Total</td>
                                    <td>{{ len(today_overviews) }}</td>
                                    <td>{{ len([o for o in today_overviews if o.last_record is not None and o.last_record.date == today]) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    % else:
                        % models = sorted({o.bus.model for o in today_overviews if o.bus.model is not None})
                        % model_types = sorted({m.type for m in models})
                        
                        <table>
                            <thead>
                                <tr>
                                    <th>Model</th>
                                    <th>Seen</th>
                                    <th>Tracked</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for type in model_types:
                                    % type_overviews = [o for o in today_overviews if o.bus.model is not None and o.bus.model.type == type]
                                    <tr class="header">
                                        <td>{{ type }}</td>
                                        <td>{{ len(type_overviews) }}</td>
                                        <td>{{ len([o for o in type_overviews if o.last_record is not None and o.last_record.date == today]) }}</td>
                                    </tr>
                                    <tr class="display-none"></tr>
                                    % type_models = [m for m in models if m.type == type]
                                    % for model in type_models:
                                        % model_overviews = [o for o in type_overviews if o.bus.model == model]
                                        <tr>
                                            <td>{{! model }}</td>
                                            <td>{{ len(model_overviews) }}</td>
                                            <td>{{ len([o for o in model_overviews if o.last_record is not None and o.last_record.date == today]) }}</td>
                                        </tr>
                                    % end
                                % end
                                <tr class="header">
                                    <td>Total</td>
                                    <td>{{ len(today_overviews) }}</td>
                                    <td>{{ len([o for o in today_overviews if o.last_record is not None and o.last_record.date == today]) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    % end
                % end
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>Last Week</h2>
            </div>
            <div class="content">
                
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>Last Month</h2>
            </div>
            <div class="content">
                
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>Last Year</h2>
            </div>
            <div class="content">
                
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>All Time</h2>
            </div>
            <div class="content">
                
            </div>
        </div>
    </div>
</div>
