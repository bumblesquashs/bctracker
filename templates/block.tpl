% rebase('base', title=f'Block {block.id}')

<h1>Block {{ block.id }}</h1>
<hr />

<div class="side-menu">
  <div class="info-box">
    <div class="info-box-header">
      <h3>Block Details</h3>
    </div>
    <div class="info-box-content">
      <div class="info-box-row">
        <span class="info-box-name">Service day(s)</span>
        <span class="info-box-value">{{ block.service }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Start time</span>
        <span class="info-box-value">{{ block.start_time }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">End time</span>
        <span class="info-box-value">{{ block.end_time }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Number of trips</span>
        <span class="info-box-value">{{ len(block.trips) }}</span>
        <br style="clear: both;" />
      </div>
      <div class="info-box-row">
        <span class="info-box-name">Route{{ '' if len(block.routes) == 1 else 's' }}</span>
        <div class="info-box-value">
          % for route in block.routes:
            <a href="{{ get_url(route.system.id, f'routes/{route.number}') }}">{{ route }}</a>
            <br />
          % end
        </div>
        <br style="clear: both;" />
      </div>
    </div>
  </div>
</div>

<div>
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
      % for trip in block.trips:
        <tr>
          <td>{{ trip.start_time }}</td>
          <td>
            {{ trip }}
            <span class="mobile-only smaller-font">
              <br />
              {{ trip.direction.value }}
            </span>
          </td>
          <td class="desktop-only">{{ trip.direction.value }}</td>
          <td><a href="{{ get_url(trip.system.id, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
        </tr>
      % end
    </tbody>
  </table>  
</div>
