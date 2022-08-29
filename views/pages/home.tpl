
% rebase('base', title='Home')

<div class="page-header">
    <h1 class="title">Welcome to BCTracker!</h1>
    % if system is None:
        <h2 class="subtitle">BC Transit Schedules and Bus Tracking</h2>
    % else:
        <h2 class="subtitle">{{ system }} Transit Schedules and Bus Tracking</h2>
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
            <p>Choose a system to search for routes and stops</p>
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
        
        <div>
            <h2>Community</h2>
            <p>
                Join the BCTracker Discord server - a home for transit riders and enthusiasts from around British Columbia!
            </p>
            <iframe src="https://discord.com/widget?id=925662392053022720&theme=dark" width="100%" height="300px" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
        </div>
    </div>
    
    <div class="flex-3">
        <h2>Latest Updates</h2>
        
        <div class="news-post">
            <div class="header">
                <h3>Summer Update</h3>
                September 1, 2022
            </div>
            <div class="content">
                <p>
                    It's been a quiet summer, so there aren't many updates to report this time around.
                </p>
                <p>
                    First, we've added <b>Mount Waddington</b> to the list of available transit systems.
                    This was never mentioned by BC Transit as a planned NextRide system, but it appears to exist nonetheless!
                </p>
                <p>
                    Second, if you use the website on your computer, you may notice that the Change System dropdown has been replaced with a shiny new sidebar.
                    We're hoping this will make it easier to navigate around the site.
                    This is still somewhat experimental, so you may see some additional changes as we get feedback.
                </p>
                <p>
                    On the topic of feedback, we have a great new place to go for that: the <a href="https://discord.gg/uMbxREE5b7">BCTracker Discord server</a>!
                    Even if you don't have any feedback, everyone is welcome to come chat, share photos and videos, debate the future of transit in BC, and more.
                    With the BCTracker Bot, you can get alerted when new buses enter service or transfer between systems.
                    And if you enjoy transit photography, we're also kicking it off with a back-to-school photo contest with special Discord roles for the winners!
                </p>
                <p>
                    That's all for now - enjoy the rest of the summer!
                </p>
            </div>
        </div>
        
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
        
        <a href="{{ get_url(system, 'news') }}">See older updates</a>
    </div>
</div>
