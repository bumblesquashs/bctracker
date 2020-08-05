% import datastructure as ds

% include('templates/header', title='Block {0}'.format(blockid))

<h1>Block {{blockid}}</h1>
<h2>Service Days: {{ds.days_of_week_dict[triplist[0].serviceid]}}</h2>
<hr />

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th>Start Time</th>
      <th>Direction</th>
      <th>Headsign</th>
      <th>Trip</th>
    </tr>
  </thead>

  <tbody>
    % triplist.sort(key=ds.trip_to_numseconds)
    % for trip in triplist:
    <tr>
      <td>{{ trip.starttime }}</td>
      <td>{{ ds.directionid_dict[trip.directionid] }}</td>
      <td>{{ trip.headsign }}</td>
      <td><a href="/trips/{{trip.tripid}}">{{ trip.tripid }}</a></td>
    </tr>
    % end
  </tbody>
</table>

% include('templates/footer')
