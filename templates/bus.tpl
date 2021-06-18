% import businfotable as businfo
% import models.realtime as rt
% import datastructure as ds
% import history as hist
% from formatting import format_date, format_date_mobile
% HISTORY_LIMIT = 20

% busrange = businfo.get_bus_range(fleetnum)
% bus_status, rt_struct = rt.get_current_status(fleetnum)
% track_history = hist.get_last_seen_bus(fleetnum)
% block_history = hist.get_block_history(fleetnum)
% last_block = hist.get_last_block_bus(fleetnum)

% rebase('base', title='Bus {0}'.format(fleetnum), include_maps=True)

<h1>Bus {{fleetnum}}</h1>
<h2>{{busrange.year}} {{busrange.model}}</h2>
<hr />

% if (bus_status == rt.STATUS_INACTIVE or bus_status == rt.STATUS_UNKNOWN_TRANSLATION or rt_struct == False):
  <h2>{{fleetnum}} is not active right now</h2>
  <p>Last updated {{rt.get_data_refreshed_time_str()}}</p>
% elif (bus_status == rt.STATUS_TRACKING):
  % include('components/map', lat=rt_struct.lat, lon=rt_struct.lon, marker_type='bus')

  <h2>{{fleetnum}} is active, but not assigned to any route</h2>
  <p>Last updated {{rt.get_data_refreshed_time_str()}}</p>
% elif (bus_status == rt.STATUS_LOGGEDIN):
  % trip = ds.tripdict[rt_struct.tripid]

  % include('components/map', lat=rt_struct.lat, lon=rt_struct.lon, shape_id=trip.shape_id, marker_type='bus')

  <h2>{{trip.headsign}}</h2>
  <p>Last updated {{rt.get_data_refreshed_time_str()}}</p>

  <p>Current stop unavailable</p>
  <p>
    <a href="/routes/{{trip.routenum}}">View Route</a><br />
    <a href="/blocks/{{rt_struct.blockid}}">View Block</a><br />
    <a href="/trips/{{rt_struct.tripid}}">View Trip</a>
  </p>
% elif (bus_status == rt.STATUS_ONROUTE):
  % trip = ds.tripdict[rt_struct.tripid]
  % stop = ds.stopdict[rt_struct.stopid]

  % include('components/map', lat=rt_struct.lat, lon=rt_struct.lon, shape_id=trip.shape_id, marker_type='bus')

  <h2>{{trip.headsign}}</h2>
  <p>Last updated {{rt.get_data_refreshed_time_str()}}</p>

  <p>Current Stop: <a href="/stops/{{stop.stopcode}}">{{stop.stopname}}</a></p>
  <p>
    <a href="/routes/{{trip.routenum}}">View Route</a><br />
    <a href="/blocks/{{rt_struct.blockid}}">View Block</a><br />
    <a href="/trips/{{rt_struct.tripid}}">View Trip</a>
  </p>
% end

<h2>Service History</h2>

% if (track_history != False):
  <p>Last seen {{ format_date(track_history['day']) }}</p>
% else:
  <p>No history for this vehicle found</p>
  <p>This site began tracking data on May 5th 2020, so vehicles retired before then will not show any history</p>
% end

% if (block_history != False):
  <p>For entries made under a older GTFS version, the block may no longer be valid</p>
  <table class="pure-table pure-table-horizontal pure-table-striped">
    <thead>
      <tr>
        <th>Date</th>
        <th>Assigned Block</th>
        <th class="desktop-only">Assigned Routes</th>
        <th class="desktop-only">Time of Day</th>
        <th class="mobile-only">Time</th>
      </tr>
    </thead>
    <tbody>
      % history_count = 0
      % block_history.reverse()
      % for block in block_history:
        % if(block['blockid'] == '0'):
          % continue # id 0 is a placeholder
        % end
        <tr>
          <td>
            <span class="desktop-only">{{ format_date(block['day']) }}</span>
            <span class="mobile-only no-wrap">{{ format_date_mobile(block['day']) }}</span>
          </td>
          <td>
            <a href="/blocks/{{block['blockid']}}">{{ block['blockid'] }}</a>
            <span class="mobile-only smaller-font">
              <br />
              {{ ', '.join(sorted(block['routes'])) }}
            </span>
          </td>
          <td class="desktop-only">{{ ', '.join(sorted(block['routes'])) }}</td>
          <td class="no-wrap">{{ hist.get_time_string(block['start_time'], block['length']) }}</td>
        </tr>
        % if(history_count > HISTORY_LIMIT):
          % break
        % end
        % history_count += 1
      % end
    </tbody>
  </table>
% elif (last_block != False): # this part is for busses that retired under the old system and only have a last block from the combined json
  <p>For entries made under a older GTFS version, the block may no longer be valid</p>
    <table class="pure-table pure-table-horizontal pure-table-striped">
      <thead>
        <tr>
          <th>Date</th>
          <th>Assigned Block</th>
          <th class="desktop-only">Assigned Routes</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <span class="desktop-only">{{ format_date(last_block['day']) }}</span>
            <span class="mobile-only no-wrap">{{ format_date_mobile(last_block['day']) }}</span>
          </td>
          <td>
            <a href="/blocks/{{last_block['blockid']}}">{{ last_block['blockid'] }}</a>
            <span class="mobile-only smaller-font">
              <br />
              {{ ', '.join(sorted(last_block['routes'])) }}
            </span>
          </td>
          <td class="desktop-only">{{ ', '.join(sorted(last_block['routes'])) }}</td>
        </tr>
      </tbody>
    </table>
% else:
  <p><i>No block history for this vehicle found...</i></p>
  % if (bus_status == rt.STATUS_UNKNOWN_TRANSLATION):
    <p><i>Note: No lookup for this fleetnumber is known, has this bus been in service lately?</i></p>
  % end
% end
