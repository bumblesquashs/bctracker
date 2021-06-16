<table class="pure-table pure-table-horizontal pure-table-striped">
	<thead>
		<tr>
			<th>System</th>
		</tr>
	</thead>
	<tbody>
		% if system is None:
			% for available_system in sorted(systems):
				<tr>
					<td><a href="{{ get_url(available_system.id, get('path', '')) }}">{{ available_system }}</a></td>
				</tr>
			% end
		% else:
			<td><a href="{{ get_url(None) }}">All Systems</a></td>
			% for available_system in sorted(systems):
				% if system != available_system:
					<tr>
						<td><a href="{{ get_url(available_system.id, get('path', '')) }}">{{ available_system }}</a></td>
					</tr>
				% end
			% end
		% end
	</tbody>
</table>
