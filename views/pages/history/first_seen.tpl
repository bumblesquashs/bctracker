
% rebase('base')

<div class="page-header">
    <h1>Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <span class="tab-button current">First Seen</span>
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
    <table>
        <thead>
            <tr>
                <th>First Seen</th>
                <th>Bus</th>
                <th class="desktop-only">Model</th>
                % if system is None:
                    <th class="non-mobile">System</th>
                % end
                <th>Block</th>
                <th class="desktop-only">Routes</th>
            </tr>
        </thead>
        <tbody>
            % last_date = None
            % for overview in overviews:
                % record = overview.first_record
                % bus = record.bus
                % order = bus.order
                % same_date = last_date is None or record.date == last_date
                % last_date = record.date
                <tr class="{{'' if same_date else 'divider'}}">
                    <td class="desktop-only">{{ record.date.format_long() }}</td>
                    <td class="non-desktop">
                        <div class="column">
                            {{ record.date.format_short() }}
                            % if system is None:
                                <span class="mobile-only smaller-font">{{ record.system }}</span>
                            % end
                        </div>
                    </td>
                    <td>
                        <div class="column">
                            % include('components/bus', bus=bus)
                            <span class="non-desktop smaller-font">
                                % include('components/order', order=order)
                            </span>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % include('components/order', order=order)
                    </td>
                    % if system is None:
                        <td class="non-mobile">{{ record.system }}</td>
                    % end
                    <td>
                        <div class="column">
                            % if record.is_available:
                                % block = record.block
                                <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
                            % else:
                                <span>{{ record.block_id }}</span>
                            % end
                            <div class="non-desktop">
                                % include('components/routes_indicator', routes=record.routes)
                            </div>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % include('components/routes_indicator', routes=record.routes)
                    </td>
                </tr>
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
