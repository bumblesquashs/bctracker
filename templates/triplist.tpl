% import datastructure as ds
% from formatting import format_time

% triplist.sort(key=ds.trip_to_numseconds)

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th class="desktop-only">Start Time</th>
      <th class="mobile-only">Start</th>
      <th>Headsign</th>
      <th class="desktop-only">Departing From</th>
      <th class="desktop-only">Block</th>
      <th>Trip</th>
    </tr>
  </thead>

  <tbody>
    %for trip in triplist:
      <tr>
        <td>{{ format_time(trip.starttime) }}</td>
        <td>{{ trip.headsign }}</td>
        <td class="desktop-only"><a href="/stops/{{ds.stopdict[trip.stoplist[0].stopid].stopcode}}">{{ trip.startstopname }}</a></td>
        <td class="desktop-only"><a href="/blocks/{{trip.blockid}}">{{ trip.blockid }}</a></td>
        <td><a href="/trips/{{trip.tripid}}">{{ trip.tripid }}</a></td>
      </tr>
    %end
  </tbody>
</table>
