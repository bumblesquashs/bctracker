% rebase('base', title='About')

<div class="page-header">
    <h1 class="title">About</h1>
</div>
<hr />

% realtime_count = len([s for s in systems if s.realtime_enabled])
% non_realtime_count = len([s for s in systems if not s.realtime_enabled])
% realtime_system_names = ', '.join([s.name for s in systems if s.realtime_enabled])

<h2>FAQs</h2>

<h3>What is BCTracker?</h3>
<p>
    BCTracker is a browser for the <a href="https://developers.google.com/transit/gtfs">GTFS (General Transit Feed Specification)</a> static and realtime data provided by <a href="https://bctransit.com">BC Transit</a>.
    The data is presented here for the use of whoever is interested, with the goal of making it easier to browse schedules and track down buses in communities around British Columbia. 
</p>

<h3>Why are only some systems available?</h3>
<p>
    When BCTracker was first created, Victoria was the only supported system.
    After some significant improvements to the website code in 2021, we began to add support for other major transit systems around the province.
    This process is still ongoing as each additional system requires more server resources and, in some cases, custom support in order to be fully integrated with the website.
</p>
<p>
    Currently we support all {{ realtime_count }} systems with realtime information and {{ non_realtime_count }} systems where only schedule data is available, with plans to add more systems in the future.
    Unfortunately, some of the smallest communities around BC do not have any GTFS information at all, so we are unable to add those systems at this time.
</p>

<h3>Why is there no transit information for Vancouver?</h3>
<p>
    As the largest metropolitan area in BC, transit in Vancouver is managed by <a href="https://www.translink.ca/">Translink</a> rather than BC Transit.
    There are numerous websites providing transit schedules and realtime information in Vancouver, including <a href="http://tcomm.bustrainferry.com/">T-Comm</a>, <a href="https://sorrybusfull.com/">Sorry Bus Full</a>, and <a href="http://www.transitdb.ca/">TransitDB</a>.
    BCTracker was developed specifically because there were no equivalent websites for the rest of the province, and we choose to leave Vancouver in good hands by those websites which are dedicated to it.
</p>

<h3>Why do only some systems have realtime information?</h3>
<p>
    Realtime information is provided by BC Transit's NextRide API, which is currently only available for {{ realtime_count }} systems: {{ ', and '.join(realtime_system_names.rsplit(', ', 1)) }}.
    Until NextRide is expanded to more communities, we unfortunately cannot include realtime for anywhere else.
</p>

<h3>How is BCTracker made?</h3>
<p>
    The website (both the pages and the data processing code) is written in Python using a simple web framework called Bottle.
    The code can be found on <a href="https://github.com/bumblesquashs/bctracker">GitHub</a> if you are interested in seeing how it works or trying to run it yourself.
</p>

<h2>Contact</h2>
<p>
    If you are curious about BCTracker, have questions, or something seems broken, you can contact us directly by emailing <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>.
    You can also join the <a href="https://discord.gg/KQX84dgfDa">Transit Vancouver Discord Server</a> where we occasionally discuss upcoming features for the website, and enjoy chatting about all things transit-related.
    Please note that the server is primarily dedicated to discussing transit in Vancouver (where we are from), but non-Vancouverites are always welcome!
</p>

<br />
<i> - James & Perrin, 2021 </i>
