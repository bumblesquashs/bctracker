
% from math import floor
% from datetime import timedelta

% from repositories import AssignmentRepository, PositionRepository, RecordRepository

% from models.date import Date

% if stops:
    % for stop in stops:
        % departures = stop.find_departures(date=Date.today())
        % routes = {d.trip.route for d in departures if d.trip and d.trip.route}
        % upcoming_count = 3 + floor(len(routes) / 3)
        % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
        % trips = [d.trip for d in upcoming_departures]
        % recorded_today = di[RecordRepository].find_recorded_today(stop.system, trips)
        % assignments = di[AssignmentRepository].find_all(stop.system, stop=stop)
        % positions = {p.trip.id: p for p in di[PositionRepository].find_all(stop.system, trip=trips)}
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <div class="column">
                    <h3>Stop {{ stop.number }} - {{ stop }}</h3>
                    <a href="{{ get_url(stop.system, f'stops/{stop.number}') }}">View stop schedule and details</a>
                </div>
                % include('components/toggle')
            </div>
            <div class="content">
                % if upcoming_departures:
                    % if not system or system.realtime_enabled:
                        <p>
                            <span>Buses with a</span>
                            <span class="scheduled">
                                % include('components/svg', name='schedule')
                            </span>
                            <span>are scheduled but may be swapped off.</span>
                        </p>
                    % end
                    <table>
                        <thead>
                            <tr>
                                <th>Time</th>
                                % if not system or system.realtime_enabled:
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
                % else:
                    % tomorrow = Date.today() + timedelta(days=1)
                    <p>
                        There are no departures for the rest of today.
                        <a href="{{ get_url(stop.system, f'stops/{stop.number}/schedule/{tomorrow.format_db()}') }}">Check tomorrow's schedule.</a>
                    </p>
                % end
            </div>
        </div>
    % end
% else:
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
% end
