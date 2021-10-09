% rebase('base', title='About')

<div class="page-header">
    <h1 class="title">About</h1>
</div>
<hr />

% realtime_count = len([s for s in systems if s.realtime_enabled])
% non_realtime_count = len([s for s in systems if not s.realtime_enabled])
<p>
    BCTracker is a browser for the <a href="https://developers.google.com/transit/gtfs">GTFS</a> static and realtime data provided by <a href="https://bctransit.com">BC Transit</a>.
    The data is presented here for the use of whoever is interested, with the goal of making it easier to browse schedules and track down buses.
    Realtime data is provided for the {{ realtime_count }} systems that currently support it, along with {{ non_realtime_count }} other systems where only schedule data is available. 
<p>

<p>
    The website (both the pages and the data processing code) is written in Python using a simple web framework called Bottle.
    The code can be found on <a href="https://github.com/bumblesquashs/bctracker">GitHub</a> if you are interested in seeing how it works or trying to run it yourself.
</p>

<p>
    If you are curious about BCTracker, have questions, or something seems broken, contact us by emailing <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>
</p>

<br />
<i> - James & Perrin, 2021 </i>
