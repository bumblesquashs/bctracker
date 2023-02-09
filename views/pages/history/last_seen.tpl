
% rebase('base', title='Vehicle History')

<div class="page-header">
    <h1 class="title">Vehicle History</h1>
    <div class="tab-button-bar">
        <span class="tab-button current">Last Seen</span>
        <a href="{{ get_url(system, 'history/first-seen') }}" class="tab-button">First Seen</a>
        <a href="{{ get_url(system, 'history/transfers') }}" class="tab-button">Transfers</a>
    </div>
    <hr />
</div>

% if system is not None and not system.realtime_enabled:
    <p>
        {{ system }} does not currently support realtime.
        You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
    </p>
% else:
    % known_overviews = [o for o in overviews if o.bus.order is not None]
    % unknown_overviews = [o for o in overviews if o.bus.order is None]
    % orders = sorted({o.bus.order for o in known_overviews})
    <table class="striped">
        <thead>
            <tr>
                <th>Bus</th>
                <th>Last Seen</th>
                % if system is None:
                    <th class="non-mobile">System</th>
                % end
                <th>Block</th>
                <th class="desktop-only">Routes</th>
            </tr>
        </thead>
        <tbody>
            % if len(unknown_overviews) > 0:
                <tr class="section">
                    <td colspan="5">
                        <div class="flex-row">
                            <div class="flex-1">Unknown Year/Model</div>
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
                            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                        </td>
                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                        <td class="non-desktop">
                            <div class="flex-column">
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
                            % if record.is_available:
                                % block = record.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % else:
                                <span>{{ record.block_id }}</span>
                            % end
                        </td>
                        <td class="desktop-only">
                            % include('components/route_indicator', routes=record.routes)
                        </td>
                    </tr>
                % end
            % end
            % for order in orders:
                % order_overviews = [o for o in known_overviews if o.bus.order == order]
                <tr class="section">
                    <td colspan="5">
                        <div class="flex-row">
                            <div class="flex-1">{{! order }}</div>
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
                            <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                        </td>
                        <td class="desktop-only">{{ record.date.format_long() }}</td>
                        <td class="non-desktop">
                            <div class="flex-column">
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
                            % if record.is_available:
                                % block = record.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % else:
                                <span>{{ record.block_id }}</span>
                            % end
                        </td>
                        <td class="desktop-only">
                            % include('components/route_indicator', routes=record.routes)
                        </td>
                    </tr>
                % end
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
