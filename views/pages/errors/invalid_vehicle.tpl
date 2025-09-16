
% rebase('base')

<div id="page-header">
    <h1>Error: {{ context.vehicle_type }} {{ vehicle_id }} Not Found</h1>
</div>

<div class="placeholder">
    <h3>The {{ context.vehicle_type.lower() }} you are looking for doesn't seem to exist!</h3>
    <p>There are a few reasons why that might be the case:</p>
    <ol>
        <li>It may be the wrong number or name - are you sure <b>{{ vehicle_id }}</b> is the one you want?</li>
        <li>It may have been retired before this tracker was started</li>
        <li>It may be a brand new {{ context.vehicle_type.lower() }} that hasn't been registered with the tracker yet</li>
    </ol>
    <p>If you believe this error is incorrect and the {{ context.vehicle_type.lower() }} actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!</p>
    
    <button class="button" onclick="window.history.back()">Back</button>
</div>
