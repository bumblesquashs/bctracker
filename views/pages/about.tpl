
% rebase('base', title='About')

<div class="page-header">
    <h1 class="title">About</h1>
    <hr />
</div>

<h2>Frequently Asked Questions</h2>
<br />

<h3>What is BCTracker?</h3>
<p>
    BCTracker is a browser for the <a href="https://developers.google.com/transit/gtfs">GTFS (General Transit Feed Specification)</a> static and realtime data provided by <a href="https://bctransit.com">BC Transit</a>.
    The data is presented here for the use of whoever is interested, with the goal of making it easier to browse schedules and track down buses in communities around British Columbia. 
</p>

<h3>How is BCTracker made?</h3>
<p>
    The website (both the pages and the data processing code) is written in Python using a simple web framework called Bottle.
    The code can be found on <a href="https://github.com/bumblesquashs/bctracker">GitHub</a> if you are interested in seeing how it works or trying to run it yourself.
</p>

<h3>Why are some transit systems not available?</h3>
<p>
    When BCTracker was first created, Victoria was the only supported transit system.
    After some significant improvements to the website code in 2021, we began to add support for other major transit systems around the province.
    This process continued with the rollout of NextRide in more transit systems in 2022, bringing support to a total of {{ len(systems) }} systems.
</p>
<p>
    Unfortunately, BC Transit does not currently provide GTFS schedules or realtime information for any of the remaining unsupported systems, which are some of the smallest in the province.
    If such information becomes available in the future, we will be sure to add those systems as soon as possible!
</p>

<h3>Why is there no transit information for Vancouver?</h3>
<p>
    Transit in Vancouver is operated by <a href="https://www.translink.ca/">Translink</a> rather than BC Transit, making it harder to integrate smoothly.
    Since long before BCTracker was started there have been numerous websites providing transit schedules and realtime information for Vancouver, including <a href="https://tcomm.bustrainferry.com/">T-Comm</a>, <a href="https://sorrybusfull.com/">Sorry Bus Full</a>, and <a href="http://www.transitdb.ca/">TransitDB</a>.
    BCTracker was developed specifically because there were no equivalent websites for the rest of the province, and we choose to leave Vancouver in the good hands of those websites which are dedicated to it.
</p>

<h2>Contact</h2>
<p>
    If you are curious about BCTracker, have questions, or something seems broken, you can contact us directly by emailing <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>.
    You can also join the <a href="https://discord.gg/KQX84dgfDa">Transit Vancouver Discord Server</a> where we occasionally discuss upcoming features for the website, and enjoy chatting about all things transit-related.
    Please note that the server is primarily dedicated to discussing transit in Vancouver (where we are from), but non-Vancouverites are always welcome!
</p>

<br />
<i> - James & Perrin, 2022 </i>
