
% import formatting

% rebase('base', title='Fleet', show_refresh_button=True)

<div class="page-header">
    <h1 class="title">Fleet</h1>
    <hr />
</div>

<table class="striped fixed-table">
    <thead>
        <tr>
            <th class="desktop-only">Number</th>
            <th class="desktop-only">Model</th>
            <th class="non-desktop">Bus</th>
            <th>Last Seen</th>
            <th class="non-mobile">System</th>
        </tr>
    </thead>
    <tbody>
        % for order in orders:
            % for number in order.range:
                % bus_number = f'{number:04d}'
                % show_divider = order != orders[0] and number == order.low
                <tr class="{{ 'divider' if show_divider else '' }}">
                    <td>
                        <a href="{{ get_url(system, f'bus/{number}') }}">{{ bus_number }}</a>
                        <br />
                        <span class="non-desktop smaller-font">{{ order }}</span>
                    </td>
                    <td class="desktop-only">
                        {{ order }}
                    </td>
                    % if number in records:
                        % record = records[number]
                        <td class="desktop-only">{{ formatting.long(record.date) }}</td>
                        <td class="non-desktop no-wrap">
                            {{ formatting.short(record.date) }}
                            % if system is None:
                                <br />
                                <span class="mobile-only smaller-font">{{ record.system }}</span>
                            % end
                        </td>
                        <td class="non-mobile">{{ record.system }}</td>
                    % else:
                        <td class="lighter-text" colspan="2">
                            Unavailable
                        </td>
                    % end
                </tr>
            % end
        % end
    </tbody>
</table>

% include('components/top_button')
