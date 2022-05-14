
% rebase('base', title='Fleet', show_refresh_button=True)

<div class="page-header">
    <h1 class="title">Fleet</h1>
    <hr />
</div>

<p>
    This is the full list of vehicles that are currently available on BCTracker.
    It does not include every bus that has ever been operated by BC Transit, but it should be mostly up-to-date with orders since the 1990s.
    Many of the older units were retired long before BCTracker was started, but are included for the sake of completion.
</p>
<p>
    Any vehicle that is marked as <span class="lighter-text">Unavailable</span> does not have any recorded history.
    There are a few reasons why that may be the case:
    <ol>
        <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
        <li>It may not have been in service since BCTracker started recording bus history</li>
        <li>It may not have functional NextRide equipment installed</li>
        <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
    </ol>
    Vehicles that do have history show the most recent date and system that they were recorded in.
</p>
% if system is not None:
    <p>
        Please note that this list includes vehicles from every system.
        To see only buses that have operated in {{ system }}, visit the <a href="{{ get_url(system, 'history') }}">history</a> page.
    </p>
% end

% model_types = sorted({o.model.type for o in orders}, key=lambda t: t.name)

<div class="button-container">
    % for type in model_types:
        <a href="#{{ type.name }}" class="button">{{ type }}</a>
    % end
</div>

<div class="container">
    % for type in model_types:
        % type_orders = [o for o in orders if o.model.type == type]
        <div id="{{ type.name }}" class="section">
            <h2 class="title">{{ type }}</h2>
            <table class="striped">
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
                    % for order in type_orders:
                        % for number in order.range:
                            % bus_number = f'{number:04d}'
                            % show_divider = order != type_orders[0] and number == order.low
                            % if number in records:
                                % record = records[number]
                                <tr class="{{ 'divider' if show_divider else '' }}">
                                    <td>
                                        <a href="{{ get_url(system, f'bus/{number}') }}">{{ bus_number }}</a>
                                        <br />
                                        <span class="non-desktop smaller-font">{{ order }}</span>
                                    </td>
                                    <td class="desktop-only">
                                        {{ order }}
                                    </td>
                                    <td class="desktop-only">{{ record.date.format_long() }}</td>
                                    <td class="non-desktop no-wrap">
                                        {{ record.date.format_short() }}
                                        % if system is None:
                                            <br />
                                            <span class="mobile-only smaller-font">{{ record.system }}</span>
                                        % end
                                    </td>
                                    <td class="non-mobile">{{ record.system }}</td>
                                </tr>
                            % else:
                                <tr class="{{ 'divider' if show_divider else '' }}">
                                    <td>
                                        {{ bus_number }}
                                        <br />
                                        <span class="non-desktop smaller-font lighter-text">{{ order }}</span>
                                    </td>
                                    <td class="desktop-only lighter-text">
                                        {{ order }}
                                    </td>
                                    <td class="lighter-text" colspan="2">Unavailable</td>
                                </tr>
                            % end
                        % end
                    % end
                </tbody>
            </table>
        </div>
    % end
</div>

% include('components/top_button')
