
% rebase('base')

<div id="page-header">
    <h1>Choose a Trip</h1>
</div>

<p>
    Multiple trips found with the ID {{ trip_id }}.
    Please select which trip you want to see.
</p>

<table>
    <thead>
        <tr>
            <th>Trip</th>
            <th class="non-mobile">System</th>
            <th>Headsign</th>
            <th class="non-mobile">Start Time</th>
            <th class="non-mobile">End Time</th>
            <th class="mobile-only">Time</th>
            <th class="desktop-only">Duration</th>
        </tr>
    </thead>
    <tbody>
        % for trip in trips:
            <tr>
                <td>
                    % include('components/trip')
                </td>
                <td class="non-mobile">{{ trip.context }}</td>
                <td>
                    <div class="column">
                        % include('components/headsign')
                        <div class="mobile-only smaller-font">{{ trip.context }}</div>
                    </div>
                </td>
                <td class="non-mobile">{{ trip.start_time }}</td>
                <td class="non-mobile">{{ trip.end_time }}</td>
                <td class="mobile-only">{{ trip.start_time }} - {{ trip.end_time }}</td>
                <td class="desktop-only">{{ trip.duration }}</td>
            </tr>
        % end
    </tbody>
</table>
