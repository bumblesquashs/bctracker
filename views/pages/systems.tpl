
% rebase('base')

<div class="page-header">
    <h1>Systems</h1>
</div>

<table>
    <thead>
        <tr>
            <th>System</th>
            <th class="desktop-only">Online</th>
            <th class="desktop-only">In Service</th>
            <th class="desktop-only">Seen</th>
            <th class="desktop-only">Tracked</th>
            <th class="desktop-only">Routes</th>
            <th class="desktop-only">Stops</th>
            <th class="desktop-only">Blocks</th>
            <th class="desktop-only">Trips</th>
            <th class="non-desktop">Details</th>
            <th class="non-mobile">Service Days</th>
        </tr>
    </thead>
    <tbody>
        % for region in regions:
            <tr class="section">
                <td class="section" colspan="11">{{ region }}</td>
            </tr>
            <tr class="display-none"></tr>
            % region_systems = sorted([s for s in systems if s.region == region])
            % for region_system in region_systems:
                <tr>
                    <td>
                        <a href="{{ get_url(region_system) }}">{{ region_system }}</a>
                    </td>
                    % if region_system.is_loaded:
                        <td class="non-desktop">
                            <div class="flex-column">
                                % if region_system.realtime_enabled:
                                    % positions = region_system.get_positions()
                                    % overviews = region_system.get_overviews()
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">Online:</span>
                                        {{ len(positions) }}
                                    </div>
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">In Service:</span>
                                        {{ len([p for p in positions if p.trip is not None]) }}
                                    </div>
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">Seen:</span>
                                        {{ len(overviews) }}
                                    </div>
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">Tracked:</span>
                                        {{ len([o for o in overviews if o.last_record is not None]) }}
                                    </div>
                                % end
                                % if region_system.gtfs_enabled:
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">Routes:</span>
                                        {{ len(region_system.get_routes()) }}
                                    </div>
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">Stops:</span>
                                        {{ len(region_system.get_stops()) }}
                                    </div>
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">Blocks:</span>
                                        {{ len(region_system.get_blocks()) }}
                                    </div>
                                    <div class="flex-row flex-gap-5">
                                        <span class="bold">Trips:</span>
                                        {{ len(region_system.get_trips()) }}
                                    </div>
                                % end
                            </div>
                        </td>
                        % if region_system.realtime_enabled:
                            <td class="desktop-only">{{ len(positions) }}</td>
                            <td class="desktop-only">{{ len([p for p in positions if p.trip is not None]) }}</td>
                            <td class="desktop-only">{{ len(overviews) }}</td>
                            <td class="desktop-only">{{ len([o for o in overviews if o.last_record is not None]) }}</td>
                        % else:
                            <td class="lighter-text desktop-only" colspan="4">Unavailable</td>
                        % end
                        % if region_system.gtfs_enabled:
                            <td class="desktop-only">{{ len(region_system.get_routes()) }}</td>
                            <td class="desktop-only">{{ len(region_system.get_stops()) }}</td>
                            <td class="desktop-only">{{ len(region_system.get_blocks()) }}</td>
                            <td class="desktop-only">{{ len(region_system.get_trips()) }}</td>
                            <td class="non-mobile">
                                % include('components/weekdays_indicator', schedule=region_system.schedule, compact=True)
                            </td>
                        % else:
                            <td class="lighter-text non-mobile" colspan="5">Unavailable</td>
                        % end
                    % else:
                        <td class="lighter-text" colspan="11">Data is loading</td>
                    % end
                </tr>
            % end
        % end
	</tbody>
</table>
