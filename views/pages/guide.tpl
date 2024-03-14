
% rebase('base')

<div id="page-header">
    <h1>Getting Started</h1>
    <h2>A Guide to BCTracker</h2>
</div>

<div class="page-container">
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>1. Choose a System</h2>
            </div>
            <div class="content">
                <p>
                    Information on BCTracker is primarily grouped by transit systems.
                    To see schedule information such as routes and stops you'll need to choose a specific system to look at.
                    Realtime information, like the main map, can be seen for individual systems or for the whole province at once.
                </p>
                <p>
                    You can select a system using the side menu on desktop computers, or by tapping the city icon in the status bar on mobile phones and tablets.
                    Currently you're looking at <b>{{ system if system else 'all systems' }}</b>.
                </p>
            </div>
        </div>
    </div>
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>2. Search</h2>
            </div>
            <div class="content">
                <p>If you're looking for something specific, like the stop near your home or your local bus route, there are two ways to search.</p>
                <h3>Quick Search</h3>
                <p>
                    Quick search is found on the <a href="{{ get_url(system) }}">Home</a> page of BCTracker.
                    You can enter your search and press enter to go directly to whatever it is you're looking for.
                    If your search can't be found, you'll see an error and you'll have to go back and try again.
                </p>
                <h3>Site-wide Search</h3>
                <p>
                    The site-wide search is available through the search button in the navigation bar on both desktop and mobile.
                    Results that match your search will appear as you type, sorted by how relevant they are.
                    Click/tap on the result you want, or press enter to go to the highlighted result.
                </p>
            </div>
        </div>
    </div>
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>3. Browse</h2>
            </div>
            <div class="content">
                <p>
                    If you aren't looking for anything specific, or you're having trouble searching for the thing you want, you can browse the schedule and realtime data instead.
                    Numerous lists and maps are available that provide an overview of all the information found on BCTracker:
                </p>
                <ul>
                    <li><a href="{{ get_url(system, 'map') }}">Map</a>: All active buses shown on a map</li>
                    <li><a href="{{ get_url(system, 'realtime') }}">Realtime</a>: All active buses shown in a list</li>
                    <li><a href="{{ get_url(system, 'history') }}">History</a>: All buses that have been tracked</li>
                    <li><a href="{{ get_url(system, 'fleet') }}">Fleet</a>: All buses known about by BCTracker</li>
                    <li><a href="{{ get_url(system, 'routes') }}">Routes List</a>: All available routes shown in a list</li>
                    <li><a href="{{ get_url(system, 'routes/map') }}">Routes Map</a>: All available routes shown on a map</li>
                    <li><a href="{{ get_url(system, 'stops') }}">Stops</a>: All available stops</li>
                    <li><a href="{{ get_url(system, 'blocks') }}">Blocks</a>: All available blocks</li>
                </ul>
            </div>
        </div>
    </div>
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>4. Explore</h2>
            </div>
            <div class="content">
                <p>
                    Once you've found something of interest, either by searching or browsing, you can see more details about it.
                    There are detail pages for buses, routes, stops, blocks, and trips.
                    These pages all have similar layouts and functionality, but with different information depending on what you're looking at.
                    You can use the tab bars at the top of each page to see additional details, such as full-screen maps, schedules for every day of the week, and comprehensive vehicle history.
                </p>
                <p>
                    All detail pages contain links to many other related pages, making it easy to get to each stop that a trip passes, see the route a bus is currently assigned to, and so on.
                    You can return to searching or browsing at any time using the links in the navigation bar/menu.
                </p>
                <p>
                    Good luck and have fun!
                </p>
            </div>
        </div>
    </div>
</div>
