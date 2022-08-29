
% rebase('base', title='Fleet')

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
    Any vehicle that is marked as <span class="lighter-text">Unavailable</span> has not been tracked.
    There are a few reasons why that may be the case:
    <ol>
        <li>It may be operating in a transit system that doesn't currently provide realtime information</li>
        <li>It may not have been in service since BCTracker started tracking buses</li>
        <li>It may not have functional NextRide equipment installed</li>
        <li>It may be operating as a HandyDART vehicle, which is not available in realtime</li>
    </ol>
    Vehicles that have been tracked before show the first and last date and system that they were seen in, even if they weren't in service.
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
                        <th>Number</th>
                        <th>First Seen</th>
                        <th class="non-mobile">First System</th>
                        <th>Last Seen</th>
                        <th class="non-mobile">Last System</th>
                    </tr>
                </thead>
                <tbody>
                    % for order in type_orders:
                        % for number in order.range:
                            % bus_number = f'{number:04d}'
                            % if number == order.low:
                                <tr class="section">
                                    <td colspan="5">{{ order }}</td>
                                </tr>
                                <tr class="display-none"></tr>
                            % end
                            % if number in overviews:
                                % overview = overviews[number]
                                <tr>
                                    <td>
                                        <a href="{{ get_url(system, f'bus/{number}') }}">{{ bus_number }}</a>
                                    </td>
                                    <td class="desktop-only">{{ overview.first_seen_date.format_long() }}</td>
                                    <td class="non-desktop no-wrap">
                                        {{ overview.first_seen_date.format_short() }}
                                        <br class="mobile-only" />
                                        <span class="mobile-only smaller-font">{{ overview.first_seen_system }}</span>
                                    </td>
                                    <td class="non-mobile">{{ overview.first_seen_system }}</td>
                                    <td class="desktop-only">{{ overview.last_seen_date.format_long() }}</td>
                                    <td class="non-desktop no-wrap">
                                        {{ overview.last_seen_date.format_short() }}
                                        <br class="mobile-only" />
                                        <span class="mobile-only smaller-font">{{ overview.last_seen_system }}</span>
                                    </td>
                                    <td class="non-mobile">{{ overview.last_seen_system }}</td>
                                </tr>
                            % else:
                                <tr>
                                    <td>{{ bus_number }}</td>
                                    <td class="lighter-text" colspan="4">Unavailable</td>
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
