
% from datetime import timedelta
% from math import floor

% rebase('base')

<div id="page-header">
    <h1>Favourites</h1>
</div>

<p>
    Add up to 20 favourites using the
    % include('components/svg', name='action/non-favourite')
    button on {{ context.vehicle_type_plural.lower() }}, routes, and stops.
</p>

% if favourites:
    % vehicle_favourites = [f for f in favourites if f.type == 'vehicle']
    % route_favourites = [f for f in favourites if f.type == 'route']
    % stop_favourites = [f for f in favourites if f.type == 'stop']
    
    <div class="container">
        % if vehicle_favourites:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>{{ context.vehicle_type_plural }}</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="page-grid">
                        % for favourite in vehicle_favourites:
                            % value = favourite.value
                            % model = value.model
                            <div class="info-box gap-10 collapsed">
                                <div class="row space-between">
                                    <div class="column">
                                        <h3 class="row">
                                            % if model and model.type:
                                                % include('components/svg', name=f'model/type/{model.type.image_name}')
                                            % end
                                            % include('components/vehicle', vehicle=value)
                                        </h3>
                                        % year_model = value.year_model
                                        % if year_model:
                                            <div>{{! year_model }}</div>
                                        % else:
                                            <div class="lighter-text">Unknown Year/Model</div>
                                        % end
                                    </div>
                                    <div class="toggle-button" onclick="toggleInfoBox(this)">
                                        % include('components/svg', name='action/dropdown')
                                    </div>
                                </div>
                                % position = vehicle_positions[value.id]
                                <div class="column stretch">
                                    % if position and position.trip:
                                        % trip = position.trip
                                        <div class="row space-between">
                                            <h3>
                                                % include('components/headsign', departure=position.departure)
                                            </h3>
                                            % include('components/adherence', adherence=position.adherence, size='large')
                                        </div>
                                        <div>
                                            % include('components/trip')
                                        </div>
                                    % else:
                                        <h3>Not In Service</h3>
                                        % allocation = vehicle_allocations[value.id]
                                        % if allocation:
                                            % if allocation.last_seen.is_today:
                                                <div class="lighter-text">Last seen today</div>
                                            % else:
                                                <div class="lighter-text">Last seen {{ allocation.last_seen.format_long() }}</div>
                                            % end
                                        % else:
                                            <div class="lighter-text">Never seen</div>
                                        % end
                                    % end
                                </div>
                                % records = vehicle_records[value.id]
                                % if records:
                                    <table class="open-only">
                                        <thead>
                                            <tr>
                                                <th>Date</th>
                                                <th class="non-mobile">System</th>
                                                % if value.context.enable_blocks:
                                                    <th>Block</th>
                                                % end
                                                <th>Routes</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % for record in records:
                                                <tr>
                                                    <td class="non-mobile">{{ record.date.format_long() }}</td>
                                                    <td class="non-mobile">{{ record.context }}</td>
                                                    <td class="mobile-only">
                                                        <div class="column">
                                                            <div>{{ record.date.format_short() }}</div>
                                                            <div class="smaller-font">{{ record.context }}</div>
                                                        </div>
                                                    </td>
                                                    % if value.context.enable_blocks:
                                                        <td>
                                                            <div class="row">
                                                                % if record.is_available:
                                                                    % block = record.block
                                                                    <a href="{{ get_url(block.context, 'blocks', block) }}">{{ block.id }}</a>
                                                                % else:
                                                                    {{ record.block_id }}
                                                                % end
                                                                % include('components/record_warnings')
                                                            </div>
                                                        </td>
                                                    % end
                                                    <td>
                                                        % include('components/route_list', routes=record.routes)
                                                    </td>
                                                </tr>
                                            % end
                                        </tbody>
                                    </table>
                                % else:
                                    <div class="placeholder open-only">
                                        <p>No recorded history</p>
                                    </div>
                                % end
                            </div>
                        % end
                    </div>
                </div>
            </div>
        % end
        % if route_favourites:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Routes</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="page-grid">
                        % for favourite in route_favourites:
                            % value = favourite.value
                            <div class="info-box gap-10 collapsed">
                                <div class="row space-between">
                                    <div class="column gap-5">
                                        <h3 class="row">
                                            % include('components/route', route=value, include_link=False)
                                            <a href="{{ get_url(value.context, 'routes', value) }}">{{! value.display_name }}</a>
                                        </h3>
                                        <div class="row">
                                            <div>{{ value.context }}</div>
                                            % include('components/weekdays', schedule=value.schedule, compact=True, schedule_path=f'routes/{value.url_id}/schedule')
                                        </div>
                                    </div>
                                    <div class="toggle-button" onclick="toggleInfoBox(this)">
                                        % include('components/svg', name='action/dropdown')
                                    </div>
                                </div>
                                % positions = route_positions[value.id]
                                % if positions:
                                    <table class="open-only">
                                        <thead>
                                            <tr>
                                                <th>{{ value.context.vehicle_type }}</th>
                                                <th class="non-mobile">Headsign</th>
                                                <th>Trip</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % for position in positions:
                                                % trip = position.trip
                                                <tr>
                                                    <td>
                                                        <div class="row">
                                                            % include('components/vehicle', vehicle=position.vehicle)
                                                            <div class="row gap-5">
                                                                % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                                % include('components/adherence', adherence=position.adherence)
                                                            </div>
                                                        </div>
                                                    </td>
                                                    <td class="non-mobile">
                                                        % include('components/headsign')
                                                    </td>
                                                    <td>
                                                        <div class="column">
                                                            % include('components/trip')
                                                            <div class="mobile-only smaller-font">
                                                                % include('components/headsign')
                                                            </div>
                                                        </div>
                                                    </td>
                                                </tr>
                                            % end
                                        </tbody>
                                    </table>
                                % else:
                                    <div class="placeholder open-only">
                                        % if value.context.realtime_enabled:
                                            <p>No active {{ value.context.vehicle_type_plural.lower() }} right now</p>
                                        % else:
                                            <p>Realtime information is not available for this route</p>
                                        % end
                                    </div>
                                % end
                            </div>
                        % end
                    </div>
                </div>
            </div>
        % end
        % if stop_favourites:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>Stops</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="page-grid">
                        % for favourite in stop_favourites:
                            % value = favourite.value
                            <div class="info-box gap-10 collapsed">
                                <div class="row space-between">
                                    <div class="column gap-5">
                                        <h3>
                                            % include('components/stop', stop=value)
                                        </h3>
                                        <div class="row">
                                            <div>{{ value.context }}</div>
                                            % include('components/route_list', routes=value.routes)
                                        </div>
                                    </div>
                                    <div class="toggle-button" onclick="toggleInfoBox(this)">
                                        % include('components/svg', name='action/dropdown')
                                    </div>
                                </div>
                                % departures = stop_departures[value.id]
                                % positions = stop_positions[value.id]
                                % assignments = stop_assignments[value.id]
                                % if departures:
                                    % upcoming_count = 3 + floor(len(value.routes) / 3)
                                    % upcoming_departures = [d for d in departures if d.time.is_now or d.time.is_later][:upcoming_count]
                                    % if upcoming_departures:
                                        <table class="open-only">
                                            <thead>
                                                <tr>
                                                    <th>Time</th>
                                                    <th class="non-mobile">Headsign</th>
                                                    <th>Trip</th>
                                                    % if value.context.realtime_enabled:
                                                        <th>{{ value.context.vehicle_type }}</th>
                                                    % end
                                                </tr>
                                            </thead>
                                            <tbody>
                                                % for departure in upcoming_departures:
                                                    % trip = departure.trip
                                                    <tr>
                                                        <td>{{ departure.time.format_web(time_format) }}</td>
                                                        <td class="non-mobile">
                                                            <div class="column">
                                                                % include('components/headsign')
                                                                % if not departure.pickup_type.is_normal:
                                                                    <span class="smaller-font italics">{{ departure.pickup_type }}</span>
                                                                % elif departure == trip.last_departure:
                                                                    <span class="smaller-font italics">No pick up</span>
                                                                % end
                                                                % if not departure.dropoff_type.is_normal:
                                                                    <span class="smaller-font italics">{{ departure.dropoff_type }}</span>
                                                                % end
                                                            </div>
                                                        </td>
                                                        <td>
                                                            <div class="column">
                                                                % include('components/trip')
                                                                <div class="mobile-only smaller-font">
                                                                    % include('components/headsign')
                                                                </div>
                                                            </div>
                                                        </td>
                                                        % if value.context.realtime_enabled:
                                                            <td>
                                                                <div class="row">
                                                                    % if trip.id in positions:
                                                                        % position = positions[trip.id]
                                                                        % include('components/vehicle', vehicle=position.vehicle)
                                                                        <div class="row gap-5">
                                                                            % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                                            % include('components/adherence', adherence=position.adherence)
                                                                        </div>
                                                                    % elif trip.block_id in assignments and trip.end_time.is_later:
                                                                        % assignment = assignments[trip.block_id]             
                                                                        % include('components/vehicle', vehicle=assignment.vehicle)
                                                                        % include('components/scheduled')
                                                                    % else:
                                                                        <span class="lighter-text">Unavailable</span>
                                                                    % end
                                                                </div>
                                                            </td>
                                                        % end
                                                    </tr>
                                                % end
                                            </tbody>
                                        </table>
                                    % else:
                                        % tomorrow = today.next()
                                        <div class="placeholder open-only">
                                            <p>
                                                There are no departures for the rest of today.
                                                <a href="{{ get_url(value.context, 'stops', value, 'schedule', tomorrow) }}">Check tomorrow's schedule.</a>
                                            </p>
                                        </div>
                                    % end
                                % end
                            </div>
                        % end
                    </div>
                </div>
            </div>
        % end
    </div>
% else:
    <div class="placeholder">
        <h3>No favourites added yet</h3>
    </div>
% end

<script>
    function toggleInfoBox(element) {
        const infoBox = element.closest(".info-box");
        infoBox.classList.toggle("collapsed");
        infoBox.classList.toggle("open");
    }
</script>
