
% rebase('base', title='Vehicle History')

<div class="page-header">
    <h1 class="title">Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <a href="{{ get_url(system, 'history/first-seen') }}" class="tab-button">First Seen</a>
        <span class="tab-button current">Transfers</span>
    </div>
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
                            % if bus.is_known:
                                <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                            % else:
                                <span>{{ bus }}</span>
                            % end
                            <span class="non-desktop smaller-font">
                                % if order is None:
                                    <span class="lighter-text">Unknown Year/Model</span>
                                % else:
                                    {{! order }}
                                % end
                            </span>
                        </div>
                    </td>
                    <td class="desktop-only">
                        % if order is None:
                            <span class="lighter-text">Unknown Year/Model</span>
                        % else:
                            {{! order }}
                        % end
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
