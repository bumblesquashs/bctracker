
% if get('realtime_only', False):
	% available_systems = [s for s in systems if s.realtime_enabled]
% else:
	% available_systems = systems
% end

% available_systems = [s for s in available_systems if not context.system or s != context.system]

<table>
	<thead>
		<tr>
			<th>System</th>
		</tr>
	</thead>
	<tbody>
		% if context.system:
			<td>
				<a href="{{ get_url(None, *path) }}">All Systems</a>
			</td>
		% end
		% for region in regions:
			% region_systems = [s for s in available_systems if s.region == region]
			% if region_systems:
				<tr class="header">
					<td>{{ region }}</td>
				</tr>
				<tr class="display-none"></tr>
				% for system in sorted(region_systems):
					% count = len(system.get_routes())
					<tr>
						<td>
							<div class="row">
								% include('components/agency_logo', agency=system.agency)
								<a href="{{ get_url(system.context, *path) }}">{{ system }}</a>
							</div>
						</td>
					</tr>
				% end
			% end
		% end
	</tbody>
</table>
