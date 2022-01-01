% rebase('base', title='Home' if system is None else 'BCTracker')

<div class="page-header">
    % if system is None:
        <h1 class="title">Welcome to BCTracker!</h1>
    % else:
        <h1 class="title">Welcome to BCTracker {{ system }}!</h1>
    % end
</div>
<hr />

<div id="sidebar">
    <h2>Quick Search</h2>
    
    <script type="text/javascript">
        function busSearch() {
            let value = document.getElementById('bus_search').value;
            if (value.length > 0) {
                window.location = "{{ get_url(system) }}/bus/" + value;
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
            <br />
            <input type="text" id="bus_search" name="bus_search" method="post">
            <input type="submit" value="Search" class="button">
        </form>
    % else:
        % if system.realtime_enabled:
            <form onsubmit="busSearch()" action="javascript:void(0)">
                <label for="bus_search">Bus Number:</label>
                <br />
                <input type="text" id="bus_search" name="bus_search" method="post">
                <input type="submit" value="Search" class="button">
            </form>
        % end
        
        <form onsubmit="routeSearch()" action="javascript:void(0)">
            <label for="route_search">Route Number:</label>
            <br />
            <input type="text" id="route_search" name="route_search" method="post">
            <input type="submit" value="Search" class="button">
        </form>
        
        <form onsubmit="stopSearch()" action="javascript:void(0)">
            <label for="stop_search">Stop Number or Name:</label>
            <br />
            <input type="text" id="stop_search" name="stop_search" method="post">
            <input type="submit" value="Search" class="button">
        </form>
    % end
    
    % if system is None:
        <p>Choose a system to search for routes and stops</p>
        % include('components/systems')
    % end
    
    <div class="theme-control">
        <h2>Theme</h2>
        <div>
            <a class="button" href="?theme=automatic">Automatic</a>
            <a class="button" href="?theme=light">Light</a>
            <a class="button" href="?theme=dark">Dark</a>
            <!-- Oh, hello there! Green and white is nice, but I wonder what the site would look like in "classic" colours. If only there was a way to set the theme to "classic"... -->
        </div>
    </div>
</div>

<div>
    <h2>Latest Updates</h2>
    
    <div class="news-post">
        <div class="header">
            <h3>Winter Update</h3>
            Date TBD
        </div>
        <div class="content">
            <p>
                Hey everyone, it's once again time for a quick update!
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
    
    <div class="news-post" id="survey">
        <div class="header">
            <h3>BCTracker Survey</h3>
            November 28, 2021
        </div>
        <div class="content">
            <p>
                We're running a quick survey over the next few weeks to get a better sense of who is using BCTracker, and for what purpose.
                This information will help us understand what new features should have the highest priority, as well as what improvements can be made to existing features.
                It's also a great opportunity for you to give us general feedback about things you like and things you think could be better.
            </p>
            <p>
                If you have a couple spare minutes, we would very much appreciate hearing from you.
                Thanks for supporting BCTracker!
            </p>
            <p>
                <button class="button survey-button" onclick="openSurvey()">Take the survey!</button>
            </p>
        </div>
    </div>
    <div class="news-post-older">
        <a href="{{ get_url(system, 'news') }}">See older updates</a>
    </div>
</div>
