% rebase('base', title=f'Block {block.id}')

<h1>Block {{ block.id }}</h1>
<h2>{{ block.service }}</h2>
<hr />

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th class="desktop-only">Start Time</th>
      <th class="mobile-only">Start</th>
      <th class=>Headsign</th>
      <th class="desktop-only">Direction</th>
      <th>Trip</th>
    </tr>
  </thead>

  <tbody>
    % for trip in sorted(block.trips):
      <tr>
        <td>{{ trip.start_time }}</td>
        <td>
          {{ trip.headsign }}
          <span class="mobile-only smaller-font">
            <br />
            {{ trip.direction.value }}
          </span>
        </td>
        <td class="desktop-only">{{ trip.direction.value }}</td>
        <td>
          <a href="{{ get_url(trip.system.id, f'/trips/{trip.id}') }}">
            {{ trip.id }}
          </a>
        </td>
      </tr>
    % end
  </tbody>
</table>
