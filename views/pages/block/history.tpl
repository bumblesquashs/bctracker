
% rebase('base', title=f'Block {block.id}')

<div class="page-header">
    <h1 class="title">Block {{ block.id }}</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, f'blocks/{block.id}') }}" class="tab-button">Overview</a>
        <a href="{{ get_url(system, f'blocks/{block.id}/map') }}" class="tab-button">Map</a>
        <span class="tab-button current">History</span>
    </div>
    <hr />
</div>

% if system.realtime_enabled:
    <div class="flex-container">
        % if len(records) > 0:
            % last_tracked = records[0].date
            % days_since_last_tracked = last_tracked.format_since()
            
            % first_tracked = records[-1].date
            % days_since_first_tracked = first_tracked.format_since()
            
            <div class="sidebar flex-1">
                <h2>Overview</h2>
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
        
        <div class="flex-3">
            <h2>History</h2>
            % if len(records) == 0:
                <p>This block doesn't have any recorded history.</p>
                <p>
                    There are a few reasons why that might be the case:
                    <ol>
                        <li>It may be a new block introduced in the last service change</li>
                        <li>It may not be operating due to driver or vehicle shortages</li>
                        <li>It may have only been done by buses without functional NextRide equipment installed</li>
                    </ol>
                    Please check again later!
                </p>
            % else:
                % if len([r for r in records if r.is_suspicious]) > 0:
                    <p>
                        <span>Buses with a</span>
                        <img class="middle-align white inline" src="/img/white/warning.png" />
                        <img class="middle-align black inline" src="/img/black/warning.png" />
                        <span>may be accidental logins.</span>
                    </p>
                % end
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
                                <td class="desktop-only">{{ record.date.format_long() }}</td>
                                <td class="non-desktop no-wrap">{{ record.date.format_short() }}</td>
                                <td>
                                    % if order is None:
                                        {{ bus }}
                                        % include('components/suspicious_record_indicator', record=record)
                                    % else:
                                        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                        % include('components/suspicious_record_indicator', record=record)
                                        <br class="non-desktop" />
                                        <span class="non-desktop smaller-font">{{ order }}</span>
                                    % end
                                </td>
                                <td class="desktop-only">
                                    % if order is not None:
                                        {{ order }}
                                    % end
                                </td>
                                <td class="non-mobile">{{ record.first_seen.format_web(time_format) }}</td>
                                <td>{{ record.last_seen.format_web(time_format) }}</td>
                            </tr>
                        % end
                    </tbody>
                </table>
            % end
        </div>
    </div>
    
    % include('components/top_button')
% else:
    <p>
        {{ system }} does not currently support realtime.
        You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
    </p>
% end
