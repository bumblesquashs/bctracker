
% rebase('base', title='Vehicle History')

<div class="page-header">
    <h1 class="title">Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <span class="tab-button current">First Seen</span>
        <a href="{{ get_url(system, 'history/transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>

% if system is not None and not system.realtime_enabled:
    <p>
        {{ system }} does not currently support realtime.
        You can browse the schedule data for {{ system }} using the links above, or choose a different system that supports realtime.
    </p>
% else:
    <table class="striped">
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
                        <div class="flex-column">
                            {{ record.date.format_short() }}
                            % if system is None:
                                <span class="mobile-only smaller-font">{{ record.system }}</span>
                            % end
                        </div>
                    </td>
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
                        % include('components/routes_indicator', routes=record.routes)
                    </td>
                </tr>
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
