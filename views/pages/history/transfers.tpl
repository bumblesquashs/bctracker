
% rebase('base', title='Vehicle History', show_refresh_button=True)

<div class="page-header">
    <h1 class="title">Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <a href="{{ get_url(system, 'history/first-seen') }}" class="tab-button">First Seen</a>
        <span class="tab-button current">Transfers</span>
    </div>
    <hr />
</div>

% if system is not None and not system.realtime_enabled:
    <p>
        {{ system }} does not currently support realtime.
        You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
    </p>
% elif len(transfers) == 0:
    % if system is None:
        <p>There are no recorded transfers.</p>
    % else:
        <p>{{ system }} does not have any recorded transfers.</p>
    % end
% else:
    <table class="striped">
        <thead>
            <tr>
                <th>Date</th>
                <th class="desktop-only">Number</th>
                <th class="desktop-only">Model</th>
                <th class="non-desktop">Bus</th>
                <th class="non-mobile">From</th>
                <th class="non-mobile">To</th>
                <th class="mobile-only">From / To</th>
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
                    <td class="non-desktop no-wrap">{{ transfer.date.format_short() }}</td>
                    <td>
                        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                        % if order is not None:
                            <br />
                            <span class="non-desktop smaller-font">{{ order }}</span>
                        % end
                    </td>
                    <td class="desktop-only">
                        % if order is not None:
                            {{ order }}
                        % end
                    </td>
                    <td class="non-mobile">{{ transfer.old_system }}</td>
                    <td class="non-mobile">{{ transfer.new_system }}</td>
                    <td class="mobile-only">From {{ transfer.old_system }} to {{ transfer.new_system }}</td>
                </tr>
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
