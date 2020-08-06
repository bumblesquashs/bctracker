% import datastructure as ds
% from formatting import format_time

% include('templates/header', title='Trip {0}'.format(tripid))

<h1>{{trip.headsign}}</h1>
<h2>Trip {{tripid}} ({{ds.days_of_week_dict[trip.serviceid]}})</h2>

<a href="/routes/{{trip.routenum}}">View Route</a>
<br />
<a href="/blocks/{{trip.blockid}}">View Block</a>
<hr />

<p>Number of stops: {{len(trip.stoplist)}}</p>

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th>Time</th>
      <th>Stop Code</th>
      <th>Stop Name</th>
    </tr>
  </thead>
  <tbody>
    % stoplist = trip.stoplist
    % for stop in stoplist:
      % stopcode = ds.stopdict[stop.stopid].stopcode
      <tr>
        <td>{{ format_time(stop.departtime) }}</td>
        <td><a href="/stops/{{stopcode}}">{{ stopcode }}</a></td>
        <td>{{ ds.stopdict[stop.stopid].stopname }}</td>
      </tr>
    % end
  </tbody>
</table>

% include('templates/footer')
