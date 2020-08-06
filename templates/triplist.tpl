% import datastructure as ds
% from formatting import format_time

% triplist.sort(key=ds.trip_to_numseconds)

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th>Start Time</th>
      <th>Headsign</th>
      <th>Departing From</th>
      <th>Block</th>
      <th>Trip</th>
    </tr>
  </thead>

  <tbody>
    %for trip in triplist:
      <tr>
        <td>{{ format_time(trip.starttime) }}</td>
        <td>{{ trip.headsign }}</td>
        <td><a href="/stops/{{ds.stopdict[trip.stoplist[0].stopid].stopcode}}">{{ trip.startstopname }}</a></td>
        <td><a href="/blocks/{{trip.blockid}}">{{ trip.blockid }}</a></td>
        <td><a href="/trips/{{trip.tripid}}">{{ trip.tripid }}</a></td>
      </tr>
    %end
  </tbody>
</table>
