% from datetime import datetime
% from formatting import format_date

% rebase('base', title=f'Stop {stop.number} - Departures', include_maps=True)

<div class="page-header">
    <h1 class="title">Stop {{ stop.number }} - Departures</h1>
    <h2 class="subtitle">{{ stop }}</h2>
    <a href="{{ get_url(system, f'stops/{stop.number}') }}">Return to stop overview</a>
</div>
<hr />

<h2>{{ format_date(datetime.now()) }}</h2>

% departures = stop.get_departures_today(sheet)
% if len(departures) > 0:
    <table class="pure-table pure-table-horizontal pure-table-striped">
        <thead>
            <tr>
                <th>Time</th>
                % if system.realtime_enabled:
                    <th>Bus</th>
                    <th class="desktop-only">Model</th>
                % end
                <th class="desktop-only">Headsign</th>
                <th class="desktop-only">Block</th>
                <th>Trip</th>
            </tr>
        </thead>
        <tbody>
            % last_hour = -1
            % for departure in departures:
                % trip = departure.trip
                % block = trip.block
                % this_hour = departure.time.hour
                % if last_hour == -1:
                    % last_hour = this_hour
                % end
                % if system.realtime_enabled:
                    % positions = block.positions
                    % if len(positions) == 0:
                        <tr class="{{'divider' if this_hour > last_hour else ''}}">
                            <td>{{ departure.time }}</td>
                            <td class="lighter-text">Unavailable</td>
                            <td class="desktop-only"></td>
                            <td class="desktop-only">
                                {{ trip }}
                                % if departure == trip.first_departure:
                                    <br />
                                    <span class="smaller-font">Loading only</span>
                                % elif departure == trip.last_departure:
                                    <br />
                                    <span class="smaller-font">Unloading only</span>
                                % end
                            </td>
                            <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                            <td>
                                <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                <span class="non-desktop smaller-font">
                                    <br />
                                    {{ trip }}
                                </span>
                            </td>
                        </tr>
                    % else:
                        % for position in positions:
                            % bus = position.bus
                            % order = bus.order
                            <tr class="{{'divider' if this_hour > last_hour else ''}}">
                                <td>{{ departure.time }}</td>
                                <td>
                                    % if position.schedule_adherence is not None:
                                        % include('components/adherence_indicator', adherence=position.schedule_adherence)
                                    % end
                                    % if bus.is_unknown:
                                        {{ bus }}
                                    % else:
                                        <a href="{{ get_url(system, f'bus/{bus.number}') }}">{{ bus }}</a>
                                    % end
                                    % if order is not None:
                                        <span class="non-desktop smaller-font">
                                            <br />
                                            {{ order }}
                                        </span>
                                    % end
                                </td>
                                <td class="desktop-only">
                                    % if order is not None:
                                        {{ order }}
                                    % end
                                </td>
                                <td class="desktop-only">
                                    {{ trip }}
                                    % if departure == trip.first_departure:
                                        <br />
                                        <span class="smaller-font">Loading only</span>
                                    % elif departure == trip.last_departure:
                                        <br />
                                        <span class="smaller-font">Unloading only</span>
                                    % end
                                </td>
                                <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                                <td>
                                    <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                                    <span class="non-desktop smaller-font">
                                        <br />
                                        {{ trip }}
                                    </span>
                                </td>
                            </tr>
                        % end
                    % end
                % else:
                    <tr class="{{'divider' if this_hour > last_hour else ''}}">
                        <td>{{ departure.time }}</td>
                        <td class="desktop-only">
                            {{ trip }}
                            % if departure == trip.first_departure:
                                <br />
                                <span class="smaller-font">Loading only</span>
                            % elif departure == trip.last_departure:
                                <br />
                                <span class="smaller-font">Unloading only</span>
                            % end
                        </td>
                        <td class="desktop-only"><a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a></td>
                        <td>
                            <a href="{{ get_url(trip.system, f'trips/{trip.id}') }}">{{ trip.id }}</a>
                            <span class="non-desktop smaller-font">
                                <br />
                                {{ trip }}
                            </span>
                        </td>
                    </tr>
                % end
                % last_hour = this_hour
            % end
        </tbody>
    </table>
% else:
    <p>There are no departures from this stop today.</p>
% end
