
% from math import floor
% from datetime import timedelta

% import helpers.position
% import helpers.record

% from models.date import Date

% if len(stops) == 0:
    <div class="section">
        <div class="placeholder">
            <h3>No stops nearby</h3>
            % if system.gtfs_loaded:
                <p>You're gonna have to walk!</p>
            % else:
                <p>System data is currently loading and will be available soon.</p>
            % end
        </div>
    </div>
% else:
    % for stop in stops:
        % departures = stop.find_departures(date=Date.today())
        % routes = {d.trip.route for d in departures if d.trip is not None and d.trip.route is not None}
        % upcoming_count = 3 + floor(len(routes) / 3)
        % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
        % trips = [d.trip for d in upcoming_departures]
        % recorded_today = helpers.record.find_recorded_today(stop.system, trips)
        % scheduled_today = helpers.record.find_scheduled_today(stop.system, trips)
        % positions = {p.trip.id: p for p in helpers.position.find_all(stop.system, trip=trips)}
        <div class="section">
            <div class="header">
                <h3>Stop {{ stop.number }} - {{ stop }}</h3>
                <a href="{{ get_url(stop.system, stop.agency, f'/stops/{stop.number}') }}">View stop schedule and details</a>
            </div>
            <div class="content">
                % if len(upcoming_departures) == 0:
                    % tomorrow = Date.today() + timedelta(days=1)
                    <p>
                        There are no departures for the rest of today.
                        <a href="{{ get_url(stop.system, stop.agency, f'/stops/{stop.number}/schedule/{tomorrow.format_db()}') }}">Check tomorrow's schedule.</a>
                    </p>
                % else:
                    % if system is None or system.realtime_enabled:
                        <p>
                            <span>Buses with a</span>
                            <img class="middle-align white" src="/img/white/schedule.png" />
                            <img class="middle-align black" src="/img/black/schedule.png" />
                            <span>are scheduled but may be swapped off.</span>
                        </p>
                    % end
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                % if system is None or system.realtime_enabled:
                                    <th>Bus</th>
                                    <th class="desktop-only">Model</th>
                                % end
                                <th class="non-mobile">Headsign</th>
                                <th class="desktop-only">Block</th>
                                <th>Trip</th>
                            </tr>
                        </thead>
                        <tbody>
                            % last_hour = -1
                            % for departure in upcoming_departures:
                                % this_hour = departure.time.hour
                                % if last_hour == -1:
                                    % last_hour = this_hour
                                % end
                                % include('rows/departure', show_divider=this_hour > last_hour)
                                % last_hour = this_hour
                            % end
                        </tbody>
                    </table>
                % end
            </div>
        </div>
    % end
% end
