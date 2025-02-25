
% rebase('base')

<div id="page-header">
    <h1>Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <span class="tab-button current">First Seen</span>
        <a href="{{ get_url(system, 'history', 'transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>

% if overviews:
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Bus</th>
                <th class="desktop-only">Model</th>
                % if not system:
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
                % if not last_date or record.date.year != last_date.year or record.date.month != last_date.month:
                    <tr class="header">
                        <td colspan="6">{{ record.date.format_month() }}</td>
                        <tr class="display-none"></tr>
                    </tr>
                % end
                % last_date = record.date
                <tr>
                    <td>
                        <div class="column">
                            {{ record.date.format_day() }}
                            % if not system:
                                <span class="mobile-only smaller-font">{{ record.system }}</span>
                            % end
                        </div>
                    </td>
                    <td>
                        <div class="column">
                            % include('components/bus')
                            <span class="non-desktop smaller-font">
                                % include('components/order', order=bus.order)
                            </span>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % include('components/order', order=bus.order)
                    </td>
                    % if not system:
                        <td class="non-mobile">{{ record.system }}</td>
                    % end
                    <td>
                        <div class="column">
                            % if record.is_available:
                                % block = record.block
                                <a href="{{ get_url(block.system, 'blocks', block) }}">{{ block.id }}</a>
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
        </tbody>
    </table>
% else:
    <div class="placeholder">
        % if not system:
            <h3>No vehicle history found</h3>
            <p>Something has probably gone terribly wrong if you're seeing this.</p>
        % elif not system.realtime_enabled:
            <h3>{{ system }} realtime information is not supported</h3>
            <p>You can browse schedule data using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % else:
            <h3>No {{ system }} buses have been recorded</h3>
            <p>Please check again later!</p>
        % end
    </div>
% end

% include('components/top_button')
