
% rebase('base', title='Home')

<div class="page-header">
    % if system is None:
        <h1 class="title">Welcome to BCTracker!</h1>
    % else:
        <h1 class="title">Welcome to BCTracker {{ system }}!</h1>
    % end
    <hr />
</div>

<div class="flex-container">
    <div class="sidebar flex-1">
        <h2>Quick Search</h2>
        
        <script type="text/javascript">
            function busSearch() {
                let value = document.getElementById('bus_search').value;
                if (value.length > 0) {
                    if (isNaN(value)) {
                        alert("Please enter a valid bus number")
                    } else {
                        window.location = "{{ get_url(system) }}/bus/" + value;
                    }
                }
            }
            
            function routeSearch() {
                let value = document.getElementById('route_search').value;
                if (value.length > 0) {
                    window.location = "{{ get_url(system) }}/routes/" + value;
                }
            }
            
            function stopSearch() {
                let value = document.getElementById('stop_search').value;
                if (value.length > 0) {
                    if (isNaN(value)) {
                        window.location = "{{ get_url(system) }}/stops?search=" + value;
                    } else {
                        window.location = "{{ get_url(system) }}/stops/" + value;
                    }
                }
            }
        </script>
        
        % if system is None:
            <form onsubmit="busSearch()" action="javascript:void(0)">
                <label for="bus_search">Bus Number:</label>
                <div class="input-container">
                    <input type="text" id="bus_search" name="bus_search" method="post" size="10">
                    <input type="submit" value="Search" class="button">
                </div>
            </form>
        % else:
            % if system.realtime_enabled:
                <form onsubmit="busSearch()" action="javascript:void(0)">
                    <label for="bus_search">Bus Number:</label>
                    <div class="input-container">
                        <input type="text" id="bus_search" name="bus_search" method="post" size="10">
                        <input type="submit" value="Search" class="button">
                    </div>
                </form>
            % end
            
            <form onsubmit="routeSearch()" action="javascript:void(0)">
                <label for="route_search">Route Number:</label>
                <div class="input-container">
                    <input type="text" id="route_search" name="route_search" method="post" size="10">
                    <input type="submit" value="Search" class="button">
                </div>
            </form>
            
            <form onsubmit="stopSearch()" action="javascript:void(0)">
                <label for="stop_search">Stop Number or Name:</label>
                <div class="input-container">
                    <input type="text" id="stop_search" name="stop_search" method="post" size="10">
                    <input type="submit" value="Search" class="button">
                </div>
            </form>
        % end
        
        % if system is None:
            <p>Choose a system to search for routes and stops</p>
            % include('components/systems')
        % end
        
        <div class="theme-control">
            <h2>Themes</h2>
            <p>
                BCTracker is available in both light and dark colours.
                You can also set it to change automatically based on your system preferences.
            </p>
            <div class="button-container">
                <a class="button" href="?theme=automatic">Automatic</a>
                <a class="button" href="?theme=light">Light</a>
                <a class="button" href="?theme=dark">Dark</a>
            </div>
            <br />
            <p>
                Alternatively, you can embrace nostalgia with themes based on older BC transit agencies.
            </p>
            <div class="button-container">
                <a class="button" href="?theme=classic">BC Transit Classic</a>
                <a class="button" href="?theme=uta">Urban Transit Authority</a>
                <a class="button" href="?theme=bchydro">BC Hydro</a>
            </div>
        </div>
    </div>
    
    <div class="flex-3">
        <h2>Latest Updates</h2>
        
        <div class="news-post">
            <div class="header">
                <h3>Spring Update</h3>
                May 1, 2022
            </div>
            <div class="content">
                <h4>New Realtime Systems</h4>
                <p>
                    Since the start of this year, BC Transit has been rolling out a new NextRide program in transit systems across BC.
                    We've been working hard to integrate the new API with BCTracker, which hasn't been easy as some of the data is quite different compared to existing systems.
                    However, we are very pleased to announce that the first new realtime systems are active on BCTracker as of today!
                </p>
                <p>
                    To start with, we're launching <b>Cowichan Valley</b>, <b>Port Alberni</b>, <b>Campbell River</b>, <b>North Okanagan</b>, and <b>Powell River</b> as brand-new realtime systems.
                    The Central Fraser Valley and Chilliwack systems have been combined into a new <b>Fraser Valley</b> system with realtime information.
                    And on top of all that, we're introducing the <b>Sunshine Coast</b> regional system with schedule-only data.
                    Expect more updates in the next few months as additional systems become available!
                </p>
                <p>
                    Please keep in mind that BC Transit is still testing some components of the new NextRide API, so you may occasionally see buses with incorrect GPS positions or logged into the wrong trip.
                    If you have any questions or concerns, feel free to reach out to us at <a href="mailto:james@bctracker.ca">james@bctracker.ca</a>.
                    For more information about the NextRide rollout and to see what systems will be receiving it next, visit <a href="https://www.bctransit.com/nextride-faq">BC Transit's NextRide FAQ</a>.
                </p>
                <h4>Other Updates</h4>
                <p>
                    Of course, new realtime systems isn't the only exciting thing we've been working on for the past few months.
                    Since we posted the last update, here's some of the other changes we've made:
                </p>
                <ul>
                    <li>Routes Map: View every route in a system on the map at the same time</li>
                    <li>Schedules: Easily check today's schedule and upcoming buses (when available) in the overview tab of stops and routes</li>
                    <li>Mobile Navigation: Updated menu makes it easier to change pages or swap to a different system</li>
                    <li>Themes: Introduced new themes based on old BC transit liveries</li>
                    <li>Lots of bug fixes and general improvements for the website interface</li>
                </ul>
                <p>
                    We hope you enjoy the new systems and improvements, and have a great summer!
                </p>
            </div>
        </div>
        
        <div class="news-post">
            <div class="header">
                <h3>Winter Update</h3>
                January 2, 2022
            </div>
            <div class="content">
                <p>
                    Hey everyone, it's once again time for a quick(ish) update!
                </p>
                <p>
                    First of all, a huge thank you to everyone who has participated in our survey so far!
                    Your feedback has been very helpful in planning upcoming additions to the site, and we're glad to know how helpful BCTracker has been for you.
                    If you haven't had a chance to respond yet, you can still get to it from the link in the previous post.
                </p>
                <p>
                    We've gotten a lot done over the last few months, some of which you may have already noticed, while other things have only just recently been added.
                    Many of the newest features are among the most highly-requested in the survey responses, so we hope you enjoy them!
                    Here's an overview of what's new:
                </p>
                <ul>
                    <li>Realtime Frequency: Now updates every minute for even more accurate bus positions</li>
                    <li>Global Search: An easy way to find buses, routes, and stops from anywhere on the website</li>
                    <li>Upcoming Departures: Trips leaving a stop in the next 30 minutes, including realtime bus information when available</li>
                    <li>Transfers and First Seen: Historic updates for when buses are transferred between systems, and when they were recorded for the first time</li>
                    <li>Block/Trip History: All recorded realtime history for blocks and trips</li>
                    <li>Map Improvements: Full-screen, interactive maps for buses, routes, stops, blocks, and trips</li>
                    <li>Some pretty big improvements behind the scenes that made a lot of these updates possible</li>
                </ul>
                <p>
                    Finally, we've updated our <a href="/about">About</a> page with some FAQs, based on some of the survey results we got back.
                    We hope the answers are enlightening!
                </p>
                <p>
                    As always, stay safe and have a Happy New Year!
                </p>
            </div>
        </div>
        
        <a href="{{ get_url(system, 'news') }}">See older updates</a>
    </div>
</div>
