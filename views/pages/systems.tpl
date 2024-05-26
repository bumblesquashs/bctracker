
% rebase('base')

<div id="page-header">
    <h1>Systems</h1>
</div>

<table>
    <thead>
        <tr>
            <th>System</th>
            <th class="desktop-only">Online</th>
            <th class="desktop-only align-right">In Service</th>
            <th class="desktop-only align-right">Seen</th>
            <th class="desktop-only align-right">Tracked</th>
            <th class="desktop-only align-right">Routes</th>
            <th class="desktop-only align-right">Stops</th>
            <th class="desktop-only align-right">Blocks</th>
            <th class="desktop-only align-right">Trips</th>
            <th class="non-desktop">Details</th>
            <th class="non-mobile">Service Days</th>
        </tr>
    </thead>
    <tbody>
        % for region in regions:
            <tr class="header">
                <td class="section" colspan="11">{{ region }}</td>
            </tr>
            <tr class="display-none"></tr>
            % region_systems = sorted([s for s in systems if s.region == region])
            % for region_system in sorted(region_systems):
                <tr>
                    <td>
                        <a href="{{ get_url(region_system) }}">{{ region_system }}</a>
                    </td>
                    <td class="non-desktop">
                        <div class="column">
                            % if region_system.realtime_enabled and region_system.realtime_loaded:
                                % positions = region_system.get_positions()
                                % overviews = region_system.get_overviews()
                                <div class="row gap-5">
                                    <span class="bold">Online:</span>
                                    {{ len(positions) }}
                                </div>
                                <div class="row gap-5">
                                    <span class="bold">In Service:</span>
                                    {{ len([p for p in positions if p.trip]) }}
                                </div>
                                <div class="row gap-5">
                                    <span class="bold">Seen:</span>
                                    {{ len(overviews) }}
                                </div>
                                <div class="row gap-5">
                                    <span class="bold">Tracked:</span>
                                    {{ len([o for o in overviews if o.last_record]) }}
                                </div>
                            % end
                            % if region_system.gtfs_enabled and region_system.gtfs_loaded:
                                <div class="row gap-5">
                                    <span class="bold">Routes:</span>
                                    {{ len(region_system.get_routes()) }}
                                </div>
                                <div class="row gap-5">
                                    <span class="bold">Stops:</span>
                                    {{ len(region_system.get_stops()) }}
                                </div>
                                <div class="row gap-5">
                                    <span class="bold">Blocks:</span>
                                    {{ len(region_system.get_blocks()) }}
                                </div>
                                <div class="row gap-5">
                                    <span class="bold">Trips:</span>
                                    {{ len(region_system.get_trips()) }}
                                </div>
                            % end
                        </div>
                    </td>
                    % if region_system.realtime_enabled:
                        % if region_system.realtime_loaded:
                            <td class="desktop-only align-right">{{ len(positions) }}</td>
                            <td class="desktop-only align-right">{{ len([p for p in positions if p.trip]) }}</td>
                            <td class="desktop-only align-right">{{ len(overviews) }}</td>
                            <td class="desktop-only align-right">{{ len([o for o in overviews if o.last_record]) }}</td>
                        % else:
                            <td class="lighter-text desktop-only" colspan="4">Data is loading</td>
                        % end
                    % else:
                        <td class="lighter-text desktop-only" colspan="4">Unavailable</td>
                    % end
                    % if region_system.gtfs_enabled:
                        % if region_system.gtfs_enabled:
                            <td class="desktop-only align-right">{{ len(region_system.get_routes()) }}</td>
                            <td class="desktop-only align-right">{{ len(region_system.get_stops()) }}</td>
                            <td class="desktop-only align-right">{{ len(region_system.get_blocks()) }}</td>
                            <td class="desktop-only align-right">{{ len(region_system.get_trips()) }}</td>
                            <td class="non-mobile">
                                % include('components/weekdays', schedule=region_system.schedule, compact=True)
                            </td>
                        % else:
                            <td class="lighter-text non-mobile" colspan="5">Data is loading</td>
                        % end
                    % else:
                        <td class="lighter-text non-mobile" colspan="5">Unavailable</td>
                    % end
                </tr>
            % end
        % end
	</tbody>
</table>
