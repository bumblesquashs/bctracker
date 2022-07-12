
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
        
        <div>
            <h2>Themes</h2>
            % if theme is None:
                <h3>Current Theme: BC Transit</h3>
            % else:
                <h3>Current Theme: {{ theme }}</h3>
            % end
            <p>
                To change the current theme, visit the <a href="{{ get_url(system, 'themes') }}">themes page</a>.
            </p>
        </div>
    </div>
    
    <div class="flex-3">
        <h2>Latest Updates</h2>
        
        <div class="news-post">
            <div class="header">
                <h3>Multiple Systems Anniversary</h3>
                July 12, 2022
            </div>
            <div class="content">
                <p>
                    Today is exactly one year since we started tracking buses in places other than Victoria.
                    We're celebrating by keeping the trend going - even more systems are now available!
                </p>
                <p>
                    Starting today, you'll find <b>East Kootenay</b>, <b>Creston Valley</b>, <b>Fort St. John</b>, <b>Dawson Creek</b>, <b>Kitimat</b>, and <b>Prince Rupert</b> in the systems list.
                    You may have also noticed the addition of <b>West Kootenay</b> as well as realtime information in <b>North Okanagan</b>, <b>South Okanagan</b>, and <b>Prince George</b> since the last update post.
                    That brings us now to a total of <b>23</b> supported systems, which is an amazing number considering that until a year ago there was only one single system!
                </p>
                <p>
                    This will likely be the last batch of new systems for a while, as BC Transit has completed the NextRide rollout in all the systems originally announced in January.
                    However, if more systems are ever introduced, rest assured that we'll work hard to get them added as well!
                </p>
                <p>
                    Happy tracking!
                </p>
            </div>
        </div>
        
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
                    To start with, we're launching <b>Cowichan Valley</b>, <b>Port Alberni</b>, <b>Campbell River</b>, <b>Powell River</b>, and <b>Sunshine Coast</b> as brand-new realtime systems.
                    The Central Fraser Valley and Chilliwack systems have also been combined into a new <b>Fraser Valley</b> system with realtime information.
                    And on top of all that, we're introducing the <b>North Okanagan</b> and <b>South Okanagan</b> regional systems with schedule-only data.
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
        
        <a href="{{ get_url(system, 'news') }}">See older updates</a>
    </div>
</div>
