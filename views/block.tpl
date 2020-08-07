% import datastructure as ds
% from formatting import format_time

% include('templates/header', title='Block {0}'.format(blockid))

<h1>Block {{blockid}}</h1>
<h2>Service Days: {{ds.days_of_week_dict[triplist[0].serviceid]}}</h2>
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
    % triplist.sort(key=ds.trip_to_numseconds)
    % for trip in triplist:
    <tr>
      <td>{{ format_time(trip.starttime) }}</td>
      <td>
        {{ trip.headsign }}
        <span class="mobile-only smaller-font">
          <br />
          {{ ds.directionid_dict[trip.directionid] }}
        </span>
      </td>
      <td class="desktop-only">{{ ds.directionid_dict[trip.directionid] }}</td>
      <td><a href="/trips/{{trip.tripid}}">{{ trip.tripid }}</a></td>
    </tr>
    % end
  </tbody>
</table>

% include('templates/footer')
