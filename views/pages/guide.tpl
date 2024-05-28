
% rebase('base')

<div id="page-header">
    <h1>Guide to BCTracker</h1>
</div>

<p>
    Welcome to BCTracker!
    This page has instructions about how to find your way around the website, along with examples.
</p>

<div class="page-container">
    <div class="container flex-3">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Getting Started</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="container">
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>Choosing a System</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                Information on BCTracker is grouped by transit systems.
                                To see schedule information such as routes and stops you'll need to choose a specific system to look at.
                                Realtime information, like the main map, can be seen for individual systems or for the whole province at once.
                            </p>
                            <p>Currently you're looking at <b>{{ system if system else 'all systems' }}</b>.</p>
                            <p>
                                <b>On Desktop:</b>
                                Select the system you want using the list on the left side of the screen.
                            </p>
                            <p>
                                <b>On Mobile/Tablet:</b>
                                Tap on the city icon in the navigation bar, then select the system you want from the list that appears.
                                If you change your mind, you can tap on the icon again to hide the systems.
                            </p>
                        </div>
                    </div>
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>Searching</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                If you're looking for something specific, like the stop near your home or your local bus route, there are two ways to search.
                                It is possible to search for buses, routes, stops and blocks.
                            </p>
                            <p>
                                <b>Quick search</b> is found on the <a href="{{ get_url(system) }}">Home</a> page of BCTracker.
                                You can enter your search and press enter to go directly to whatever it is you're looking for.
                                If your search can't be found, you'll see an error and you'll have to go back and try again.
                            </p>
                            <p>
                                <b>Site-wide search</b> is available through the search button in the navigation bar on both desktop and mobile.
                                Results that match your search will appear as you type, sorted by how relevant they are.
                                Click/tap on the result you want, or press enter to go to the highlighted result. 
                            </p>
                        </div>
                    </div>
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>Navigation</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <p>
                                Once you're looking at (for example) a route's page, it is easy to browse related information by clicking on one of the many links and tabs. 
                                A system's stops, routes, trips, blocks and buses are all connected via these links.
                            </p>
                            <p>
                                For example, on a route, you can find the list of trips for the current day. In each trip, you will find a link to the trip's block, the first stop, and even what bus will operate that trip. 
                            </p>
                            <p>
                                Clicking on a trip ID will bring you a page with extra details about that trip, such as a list of stops on the trip. There is also an interactive map of stops on the trip, and even historical records of what bus 
                                has operated that trip, all of which may be explored further.
                            </p>
                            <p>
                                If you are interested in seeing what trips will run on other days, you can click the schedule tab at the top, which lets you browse the schedule for each day of the week, and even 
                                which days have special service (and what that special schedule is!).
                            </p>
                            <p>
                                Finally, if you were interested in seeing what trips the bus does before or after one of these trips, you might click on the block number, which will tell you what other trips will be run by the same bus.
                            </p>
                            <p>
                                The site has many ways of displaying the schedule data - you are encouraged to explore around with the tabs and links to find what you are interested in.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>How To...</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="container">
                    <div class="section">
                        <div class="header" onclick="toggleSection(this)">
                            <h3>Find the schedule for a stop?</h3>
                            % include('components/toggle')
                        </div>
                        <div class="content">
                            <ol>
                                <li>
                                    Start by navigating to the page for the stop
                                    <ul>
                                        <li>If you know the stop number, you can search for it directly</li>
                                        <li>If you don't know the number, you can also search for the name of the stop - usually this is an intersection (eg. Douglas St at Fort St) or an important location (eg. Lansdowne Exchange)</li>
                                        <li>If you don't know the number or name, but you know what route it's on, navigate to the route page and go to the Map tab, then click on the stop icon. Alternatively, choose a trip from the list and browse its list of stops.</li>
                                    </ul>
                                </li>
                                <li>The current schedule for the stop will be shown on the main Overview</li>
                                <li>A list of upcoming departures, with realtime updates, will also be displayed (if available).</li>
                                <li>To see the schedule for a different day, click on the Schedule tab and select the day you want to see</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Definitions</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="section">
                        <h4>Transit System</h4>
                        <p>
                            A city or region with a network of transit routes and a dedicated bus fleet.
                            Some transit systems may provide interregional connections to other nearby systems.
                        </p>
                    </div>
                    <div class="section">
                        <h4>Block</h4>
                        <p>
                            A set of consecutive trips that a bus is assigned to operate.
                            Blocks may cover one route or multiple, and may be as short as one trip or span an entire day.
                        </p>
                    </div>
                    <div class="section">
                        <h4>Transfer</h4>
                        <p>
                            A transfer occurs when a bus is moved from one transit system to another.
                            This may occur because of a change in service requirements, to cover for buses undergoing maintenance, or many other reasons.
                        </p>
                    </div>
                    <div class="section">
                        <h4>Special Service</h4>
                        <p>
                            A day or set of days when the schedule for a route or stop is different from normal.
                            This may be due to additional, reduced, or rescheduled service.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
