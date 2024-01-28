
% rebase('base')

<div class="page-header">
    <h1 class="title">Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <a href="{{ get_url(system, 'history/first-seen') }}" class="tab-button">First Seen</a>
        <span class="tab-button current">Transfers</span>
    </div>
</div>

% if len(transfers) == 0:
    <div class="placeholder">
        % if system is None:
            <h3>No transfers found</h3>
            <p>Something has probably gone terribly wrong if you're seeing this.</p>
        % elif not system.realtime_enabled:
            <h3>{{ system }} does not currently support realtime</h3>
            <p>You can browse the schedule data for {{ system }} using the links above, or choose a different system.</p>
            <div class="non-desktop">
                % include('components/systems')
            </div>
        % else:
            <h3>No buses have been transferred to or from {{ system }}</h3>
            <p>Please check again later!</p>
        % end
    </div>
% else:
    <table class="striped">
        <thead>
            <tr>
                <th>Date</th>
                <th>Bus</th>
                <th class="desktop-only">Model</th>
                <th class="non-mobile">From</th>
                <th class="non-mobile">To</th>
                <th class="mobile-only">Systems</th>
            </tr>
        </thead>
        <tbody>
            % last_date = None
            % for transfer in transfers:
                % bus = transfer.bus
                % order = bus.order
                % same_date = last_date is None or transfer.date == last_date
                % last_date = transfer.date
                <tr class="{{'' if same_date else 'divider'}}">
                    <td class="desktop-only">{{ transfer.date.format_long() }}</td>
                    <td class="non-desktop">{{ transfer.date.format_short() }}</td>
                    <td>
                        <div class="flex-column">
                            % include('components/bus', bus=bus)
                            <span class="non-desktop smaller-font">
                                % include('components/order', order=order)
                            </span>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % include('components/order', order=order)
                    </td>
                    <td class="non-mobile">{{ transfer.old_system }}</td>
                    <td class="non-mobile">{{ transfer.new_system }}</td>
                    <td class="mobile-only">
                        <div class="flex-column">
                            <div>
                                <div class="smaller-font">From:</div>
                                {{ transfer.old_system }}
                            </div>
                            <div>
                                <div class="smaller-font">To:</div>
                                {{ transfer.new_system }}
                            </div>
                        </div>
                    </td>
                </tr>
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
