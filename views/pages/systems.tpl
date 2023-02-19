
% rebase('base', title='Systems', enable_refresh=False)

<div class="page-header">
    <h1 class="title">Systems</h1>
    <hr />
</div>

<table class="striped">
	<thead>
		<tr>
			<th>System</th>
            <th>Online</th>
            <th>In Service</th>
            <th>Routes</th>
            <th>Stops</th>
            <th>Blocks</th>
            <th>Trips</th>
            <th>Service Days</th>
		</tr>
	</thead>
	<tbody>
        % for region in regions:
            <tr class="section">
                <td class="section" colspan="8">{{ region }}</td>
            </tr>
            <tr class="display-none"></tr>
            % region_systems = sorted([s for s in systems if s.region == region])
            % for region_system in region_systems:
                <tr>
                    <td><a href="{{ get_url(region_system) }}">{{ region_system }}</a></td>
                    % if region_system.realtime_enabled:
                        % positions = region_system.get_positions()
                        <td>{{ len(positions) }}</td>
                        <td>{{ len([p for p in positions if p.trip is not None]) }}</td>
                    % else:
                        <td class="lighter-text" colspan="2">Unavailable</td>
                    % end
                    % if region_system.gtfs_enabled:
                        <td>{{ len(region_system.get_routes()) }}</td>
                        <td>{{ len(region_system.get_stops()) }}</td>
                        <td>{{ len(region_system.get_blocks()) }}</td>
                        <td>{{ len(region_system.get_trips()) }}</td>
                        <td>
                            % include('components/weekdays_indicator', schedule=region_system.schedule, compact=True)
                        </td>
                    % else:
                        <td class="lighter-text" colspan="5">Unavailable</td>
                    % end
                </tr>
            % end
        % end
	</tbody>
</table>
