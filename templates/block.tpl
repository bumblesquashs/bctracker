% rebase('base', title=f'Block {block.id}')

<h1>Block {{ block.id }}</h1>
<hr />

<div class="sidebar">
  <div class="info-box">
    <div class="info-box-section">
      % services = block.services
      % if len(services) == 1:
        % include('components/service_indicator', service=services[0])
      % else:
        % include('components/services_indicator', services=services)
      % end
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Start time</div>
      <div class="info-box-value">{{ block.start_time }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">End time</div>
      <div class="info-box-value">{{ block.end_time }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Number of trips</div>
      <div class="info-box-value">{{ len(block.available_trips) }}</div>
    </div>
    <div class="info-box-section">
      <div class="info-box-name">Route{{ '' if len(block.routes) == 1 else 's' }}</div>
      <div class="info-box-value">
        % for route in block.routes:
          <a href="{{ get_url(route.system, f'routes/{route.number}') }}">{{ route }}</a>
          <br />
        % end
      </div>
    </div>
  </div>
</div>

<div class="body">
  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th class="desktop-only">Start Time</th>
        <th class="desktop-only">End Time</th>
        <th class="mobile-only">Start</th>
        <th class=>Headsign</th>
        <th class="desktop-only">Direction</th>
        <th>Trip</th>
      </tr>
    </thead>
  
    <tbody>
      % for trip in block.available_trips:
        <tr>
          <td>{{ trip.start_time }}</td>
          <td class="desktop-only">{{ trip.end_time }}</td>
          <td>
            {{ trip }}
            <span class="mobile-only smaller-font">
              <br />
              {{ trip.direction }}
            </span>
          </td>
          <td class="desktop-only">{{ trip.direction }}</td>
          <td><a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a></td>
        </tr>
      % end
    </tbody>
  </table>  
</div>
