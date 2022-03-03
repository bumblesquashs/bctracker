% import formatting

% rebase('base', title='Vehicle History')

<div class="page-header">
    <h1 class="title">Vehicle History</h1>
    <div class="tab-button-bar">
        <a href="{{ get_url(system, 'history') }}" class="tab-button">Last Seen</a>
        <span class="tab-button current">First Seen</span>
        <a href="{{ get_url(system, 'history/transfers') }}" class="tab-button">Transfers</a>
    </div>
</div>
<hr />

% if system is not None and not system.realtime_enabled:
    <p>
        {{ system }} does not currently support realtime.
        You can browse the schedule data for {{ system }} using the links above, or choose another system that supports realtime from the following list.
    </p>
    
    % include('components/systems', realtime_only=True)
% else:
    <table class="striped">
        <thead>
            <tr>
                <th>First Seen</th>
                <th class="desktop-only">Number</th>
                <th class="desktop-only">Model</th>
                <th class="non-desktop">Bus</th>
                % if system is None:
                    <th class="non-mobile">System</th>
                % end
                <th class="desktop-only">Assigned Block</th>
                <th class="desktop-only">Assigned Routes</th>
                <th class="non-desktop">Block</th>
            </tr>
        </thead>
        <tbody>
            % last_date = None
            % for record in records:
                % bus = record.bus
                % order = bus.order
                % same_date = last_date is None or record.date == last_date
                % last_date = record.date
                <tr class="{{'' if same_date else 'divider'}}">
                    <td class="desktop-only">{{ formatting.long(record.date) }}</td>
                    <td class="non-desktop no-wrap">{{ formatting.short(record.date) }}</td>
                    <td>
                        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                        % if order is not None:
                            <span class="non-desktop smaller-font">
                                <br />
                                {{ order }}
                            </span>
                        % end
                    </td>
                    <td class="desktop-only">
                        % if order is not None:
                            {{ order }}
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
                    <td class="desktop-only">{{ record.routes }}</td>
                </tr>
            % end
        </tbody>
    </table>
% end

% include('components/top_button')
