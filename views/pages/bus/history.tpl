
% from models.model import ModelType

% rebase('base')

% model = bus.model

<div id="page-header">
    <h1 class="row">
        % if model:
            % title_prefix = model.type.title_prefix
            % if title_prefix:
                <span>{{ title_prefix }}</span>
            % end
        % end
        % include('components/bus', enable_link=False)
        % include('components/favourite')
    </h1>
    % year_model = bus.year_model
    % if year_model:
        <h2>{{! year_model }}</h2>
    % else:
        <h2 class="lighter-text">Unknown Year/Model</h2>
    % end
    <div class="tab-button-bar">
        <a href="{{ get_url(context, 'bus', bus) }}" class="tab-button">Overview</a>
        <a href="{{ get_url(context, 'bus', bus, 'map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
</div>

<div class="page-container">
    % if allocations:
        <div class="sidebar container flex-1">
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Overview</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="info-box">
                        <div class="section">
                            % include('components/events_list', events=events)
                        </div>
                        <div class="row section">
                            <div class="name">Total Records</div>
                            <div class="value">{{ total_items }}</div>
                        </div>
                        <h3>Allocation History</h3>
                        % for allocation in allocations:
                            <div class="section">
                                <a href="{{ get_url(allocation.context) }}">{{ allocation.context }}</a>
                                <div class="smaller-font ligher-text">
                                    {{ allocation.first_seen.format_long() }} - {{ allocation.last_seen.format_long() }}
                                </div>
                            </div>
                        % end
                    </div>
                </div>
            </div>
        </div>
    % end
    
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>History</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                % if total_items == 0:
                    <div class="placeholder">
                        <h3>This {{ context.realtime_vehicle_type.lower() }} doesn't have any recorded history</h3>
                        <p>There are a few reasons why that might be the case:</p>
                        <ol>
                            <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
                            <li>It may not have been in service since BCTracker started recording {{ context.realtime_vehicle_type.lower() }} history</li>
                            <li>It may not have functional tracking equipment installed</li>
                            % model = bus.model
                            % if model is None or model.type == ModelType.shuttle:
                                <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
                            % end
                        </ol>
                        <p>Please check again later!</p>
                    </div>
                % else:
                    % if records:
                        % include('components/paging')
                        
                        % dates = {r.date for r in records}
                        <h3>{{ min(dates).format_long() }} - {{ max(dates).format_long() }}</h3>
                        
                        % if any(r.warnings for r in records):
                            <p>
                                <span>Entries with a</span>
                                <span class="record-warnings">
                                    % include('components/svg', name='status/warning')
                                </span>
                                <span>may be accidental logins.</span>
                            </p>
                        % end
                        <div class="table-border-wrapper">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th class="desktop-only">System</th>
                                        % if context.enable_blocks:
                                            <th>Block</th>
                                            <th class="desktop-only">Routes</th>
                                        % else:
                                            <th>Routes</th>
                                        % end
                                        <th class="desktop-only">Start Time</th>
                                        <th class="desktop-only">End Time</th>
                                        <th class="no-wrap non-mobile">First Seen</th>
                                        <th class="no-wrap">Last Seen</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    % last_date = None
                                    % for record in records:
                                        % if not last_date or record.date.year != last_date.year or record.date.month != last_date.month:
                                            <tr class="header">
                                                <td colspan="8">{{ record.date.format_month() }}</td>
                                                <tr class="display-none"></tr>
                                            </tr>
                                        % end
                                        % last_date = record.date
                                        <tr>
                                            <td>
                                                <div class="column">
                                                    {{ record.date.format_day() }}
                                                    <span class="non-desktop smaller-font">{{ record.context }}</span>
                                                </div>
                                            </td>
                                            <td class="desktop-only">{{ record.context }}</td>
                                            % if context.enable_blocks:
                                                <td>
                                                    <div class="column stretch">
                                                        <div class="row space-between">
                                                            % if record.is_available:
                                                                % block = record.block
                                                                <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
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
                                            % else:
                                                <td>
                                                    % include('components/route_list', routes=record.routes)
                                                </td>
                                            % end
                                            <td class="desktop-only">{{ record.start_time.format_web(time_format) }}</td>
                                            <td class="desktop-only">{{ record.end_time.format_web(time_format) }}</td>
                                            <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                            <td>{{ record.last_seen.format_web(time_format) }}</td>
                                        </tr>
                                    % end
                                </tbody>
                            </table>
                        </div>
                        % include('components/paging')
                    % else:
                        <div class="placeholder">
                            % if page == 0:
                                <h3>Page {{ page }} does not exist...?</h3>
                                <p>If you're a software developer you may be thinking right now, "Hey, wait a minute, why doesn't this list start at 0?!‽"</p>
                                <p>
                                    Look, we agree with you, it feels weird to be showing this error message at all.
                                    Sadly too many people are expecting page 1 to be the first because "it makes more sense" or "0 isn't a real number" or something equally silly.
                                    But you should know that we're right and they're just mad about it.
                                </p>
                                <p>Unfortunately you do still need to return to a <a href="?page=1">valid page</a> but remember that one day the zero-based indexers shall rise up and claim our rightful place once and for all!</p>
                            % else:
                                <h3>Page {{ page }} does not exist!</h3>
                                <p>If you got to this page through <i>nefarious tomfoolery</i> or <i>skullduggery</i>, please return to a <a href="?page=1">valid page</a>, then go sit in a corner and think about what you've done.</p>
                                <p>
                                    If you got to this page by accident, we're very sorry.
                                    Please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!
                                </p>
                            % end
                        </div>
                    % end
                % end
            </div>
        </div>
    </div>
</div>

% include('components/top_button')
