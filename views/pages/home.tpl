
% rebase('base')

<div class="page-header">
    <h1 class="title">Welcome to BCTracker!</h1>
    % if system is None:
        <h2 class="subtitle">BC Transit Schedules and Bus Tracking</h2>
    % else:
        <h2 class="subtitle">{{ system }} Transit Schedules and Bus Tracking</h2>
    % end
</div>

<div class="flex-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header">
                <h2>Quick Search</h2>
            </div>
            <div class="content">
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
                    
                    function blockSearch() {
                        let value = document.getElementById('block_search').value;
                        if (value.length > 0) {
                            window.location = "{{ get_url(system) }}/blocks/" + value;
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
                    
                    <form onsubmit="blockSearch()" action="javascript:void(0)">
                        <label for="block_search">Block ID:</label>
                        <div class="input-container">
                            <input type="text" id="block_search" name="block_search" method="post" size="10">
                            <input type="submit" value="Search" class="button">
                        </div>
                    </form>
                % end
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>Community</h2>
            </div>
            <div class="section">
                <p class="margin-bottom-10">
                    Join the BCTracker Discord server - a home for transit riders and enthusiasts from around British Columbia!
                </p>
                <iframe src="https://discord.com/widget?id=925662392053022720&theme=dark" width="100%" height="300px" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
            </div>
        </div>
    </div>
    
    <div class="container flex-3">
        <div class="section">
            <div class="header">
                <h2>Quick Navigation</h2>
            </div>
            <div class="content">
                <div id="quick-navigation">
                    <div class="item">
                        <img class="white" src="/img/white/realtime.png" />
                        <img class="black" src="/img/black/realtime.png" />
                        <h3>Bus Tracking</h3>
                        <p class="margin-bottom-10">
                            See all buses that are currently active, including current route and location
                        </p>
                        <div class="button-container">
                            <a class="button" href="{{ get_url(system, 'realtime') }}">List</a>
                            <a class="button" href="{{ get_url(system, 'map') }}">Map</a>
                        </div>
                    </div>
                    <div class="item">
                        <img class="white" src="/img/white/history.png" />
                        <img class="black" src="/img/black/history.png" />
                        <h3>Bus History</h3>
                        <p class="margin-bottom-10">
                            See all buses that have been tracked, including last-seen date and transfers
                        </p>
                        <div class="button-container">
                            <a class="button" href="{{ get_url(system, 'history') }}">History</a>
                            <a class="button" href="{{ get_url(system, 'history/transfers') }}">Transfers</a>
                        </div>
                    </div>
                    <div class="item">
                        <img class="white" src="/img/white/route.png" />
                        <img class="black" src="/img/black/route.png" />
                        <h3>Schedules and Maps</h3>
                        <p class="margin-bottom-10">
                            See departure times and routing details for routes, stops, blocks, and more
                        </p>
                        <div class="button-container">
                            <a class="button" href="{{ get_url(system, 'routes') }}">Routes</a>
                            <a class="button" href="{{ get_url(system, 'stops') }}">Stops</a>
                            <a class="button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="header">
                <h2>Latest News</h2>
            </div>
            <div class="content">
                <div class="container">
                    <div class="news-post">
                        <div class="header">
                            <h3>BCTracker Survey</h3>
                            December 18, 2023
                        </div>
                        <div class="content">
                            <p>
                                We're running a quick survey over the next few weeks to get a better sense of who is using BCTracker, and for what purpose.
                                This information will help us understand what new features should have the highest priority, as well as what improvements can be made to existing features.
                                It's also a great opportunity for you to give us general feedback about things you like and things you think could be better.
                            </p>
                            <p>
                                If you've been here long enough, you may remember a similar survey we ran in 2021.
                                It was very helpful for us and since then we've addressed nearly every suggestion and request!
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
                    <div class="news-post">
                        <div class="header">
                            <h3>Summer Update</h3>
                            August 15, 2023
                        </div>
                        <div class="content">
                            <p>
                                It's been a while since we posted anything here!
                                These days most updates and announcements are being done over on our <a href="https://discord.gg/uMbxREE5b7">Discord server</a>, but now seems like a good time for a brief mention of some of the changes we've made since the last update post.
                            </p>
                            <p>
                                We've focused a lot on polishing up the website and making it easier to use, especially on mobile phones.
                                This includes stuff like:
                            </p>
                            <ul>
                                <li>Improving website layout on small screens</li>
                                <li>Adding more route colour boxes and lines</li>
                                <li>Introducing the Quick Navigation section to the homepage</li>
                            </ul>
                            <p>
                                We've also been adding many new and improved features, such as:
                            </p>
                            <ul>
                                <li>Upcoming departures on stop pages</li>
                                <li>Warning indicators for incorrect bus logins</li>
                                <li>Total distance travelled for blocks and trips</li>
                            </ul>
                            <p>
                                And finally, we've been fixing a bunch of bugs and making some big changes behind the scenes that will let us keep adding fun and helpful new features.
                                Stay tuned for more coming soon, and have a great rest of the summer!
                            </p>
                        </div>
                    </div>
                    <div>
                        <a href="{{ get_url(system, 'news') }}">See older news</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
