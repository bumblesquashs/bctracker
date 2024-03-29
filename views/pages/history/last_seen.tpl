
% rebase('base')

<div id="page-header">
    <h1>Vehicle History</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Last Seen</span>
        <a href="{{ get_url(system, 'history/first-seen') }}" class="tab-button">First Seen</a>
        <a href="{{ get_url(system, 'history/transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>

% if len(overviews) == 0:
    <div class="placeholder">
        % if system is None:
            <h3>No vehicle history found</h3>
            <p>Something has probably gone terribly wrong if you're seeing this.</p>
        % elif not system.realtime_enabled:
            <h3>{{ system }} does not currently support realtime</h3>
            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % else:
            <h3>No buses have been recorded in {{ system }}</h3>
            <p>Please check again later!</p>
        % end
    </div>
% else:
    % known_overviews = [o for o in overviews if o.bus.order is not None]
    % unknown_overviews = [o for o in overviews if o.bus.order is None]
    % orders = sorted({o.bus.order for o in known_overviews})
    <table>
        <thead>
            <tr>
                <th>Bus</th>
                <th>Last Seen</th>
                % if system is None:
                    <th class="non-mobile">System</th>
                % end
                % if af_2024:
                    <th>Trip</th>
                % else:
                    <th>Block</th>
                % end
                <th class="desktop-only">Routes</th>
            </tr>
        </thead>
        <tbody>
            % if len(unknown_overviews) > 0:
                <tr class="header">
                    <td colspan="5">
                        <div class="row space-between">
                            <div>Unknown Year/Model</div>
                            <div>{{ len(unknown_overviews) }}</div>
                        </div>
                    </td>
                </tr>
                <tr class="display-none"></tr>
                % for overview in unknown_overviews:
                    % record = overview.last_record
                    % bus = overview.bus
                    <tr>
                        <td>
                            % include('components/bus')
                        </td>
                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                        <td class="non-desktop">
                            <div class="column">
                                {{ record.date.format_short() }}
                                % if system is None:
                                    <span class="mobile-only smaller-font">{{ record.system }}</span>
                                % end
                            </div>
                        </td>
                        % if system is None:
                            <td class="non-mobile">{{ record.system }}</td>
                        % end
                        <td>
                            <div class="column">
                                % if record.is_available:
                                    % block = record.block
                                    % if af_2024:
                                        <a href="{{ get_url(block.system, f'trips/{block.id}') }}">{{ block }}</a>
                                    % else:
                                        % include('components/block')
                                    % end
                                % else:
                                    <span>{{ record.block_id }}</span>
                                % end
                                <div class="non-desktop">
                                    % include('components/route_list', routes=record.routes)
                                </div>
                            </div>
                        </td>
                        <td class="desktop-only">
                            % include('components/route_list', routes=record.routes)
                        </td>
                    </tr>
                % end
            % end
            % for order in orders:
                % order_overviews = [o for o in known_overviews if o.bus.order == order]
                <tr class="header">
                    <td colspan="5">
                        <div class="row space-between">
                            <div>{{! order }}</div>
                            <div>{{ len(order_overviews) }}</div>
                        </div>
                    </td>
                </tr>
                <tr class="display-none"></tr>
                % for overview in order_overviews:
                    % record = overview.last_record
                    % bus = overview.bus
                    <tr>
                        <td>
                            % include('components/bus')
                        </td>
                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                        <td class="non-desktop">
                            <div class="column">
                                {{ record.date.format_short() }}
                                % if system is None:
                                    <span class="mobile-only smaller-font">{{ record.system }}</span>
                                % end
                            </div>
                        </td>
                        % if system is None:
                            <td class="non-mobile">{{ record.system }}</td>
                        % end
                        <td>
                            <div class="column">
                                % if record.is_available:
                                    % block = record.block
                                    % if af_2024:
                                        <a href="{{ get_url(block.system, f'trips/{block.id}') }}">{{ block }}</a>
                                    % else:
                                        % include('components/block')
                                    % end
                                % else:
                                    <span>{{ record.block_id }}</span>
                                % end
                                <div class="non-desktop">
                                    % include('components/route_list', routes=record.routes)
                                </div>
                            </div>
                        </td>
                        <td class="desktop-only">
                            % include('components/route_list', routes=record.routes)
                        </td>
                    </tr>
                % end
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
