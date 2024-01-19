
% if get('realtime_only', False):
	% available_systems = [s for s in systems if s.realtime_enabled]
% else:
	% available_systems = systems
% end

% available_systems = [s for s in available_systems if system is None or s != system]

<table>
	<thead>
		<tr>
			<th>System</th>
		</tr>
	</thead>
	<tbody>
		% if system is not None:
			<td>
				<a href="{{ get_url(None, path) }}">All Systems</a>
			</td>
		% end
		% for region in regions:
			% region_systems = [s for s in available_systems if s.region == region]
			% if len(region_systems) > 0:
				<tr class="header">
					<td>{{ region }}</td>
				</tr>
				<tr class="display-none"></tr>
				% for region_system in region_systems:
					% count = len(region_system.get_routes())
					<tr>
						<td>
							<a href="{{ get_url(region_system, path) }}">{{ region_system }}</a>
						</td>
					</tr>
				% end
			% end
		% end
	</tbody>
</table>
