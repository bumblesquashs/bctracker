
% rebase('base')

<div id="page-header">
    <h1>Welcome to BCTracker!</h1>
    % if system is None:
        <h2>BC Transit Schedules and Bus Tracking</h2>
    % else:
        <h2>{{ system }} Transit Schedules and Bus Tracking</h2>
    % end
</div>

<div class="page-container">
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
                <h2>Quick Navigation</h2>
            </div>
            <div class="content">
                <p>
                    New to BCTracker?
                    Check out our <a href="{{ get_url(system, 'guide') }}">Getting Started</a> guide!
                </p>
                <div id="quick-navigation">
                    <div class="item">
                        <div class="column center">
                            <img class="white" src="/img/white/realtime.png" />
                            <img class="black" src="/img/black/realtime.png" />
                            <h3>Bus Tracking</h3>
                            <p>See all buses that are currently active, including current route and location</p>
                        </div>
                        <div class="button-container">
                            <a class="button" href="{{ get_url(system, 'realtime') }}">List</a>
                            <a class="button" href="{{ get_url(system, 'map') }}">Map</a>
                            <a class="button" href="{{ get_url(system, 'history') }}">History</a>
                        </div>
                    </div>
                    <div class="item">
                        <div class="column center">
                            <img class="white" src="/img/white/route.png" />
                            <img class="black" src="/img/black/route.png" />
                            <h3>Schedules and Maps</h3>
                            <p>See departure times and routing details for routes, stops, blocks, and more</p>
                        </div>
                        <div class="button-container">
                            <a class="button" href="{{ get_url(system, 'routes') }}">Routes</a>
                            <a class="button" href="{{ get_url(system, 'stops') }}">Stops</a>
                            <a class="button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container flex-2">
        <div class="section">
            <div class="header">
                <h2>Latest News</h2>
            </div>
            <div class="content">
                <div class="container">
                    <div class="news-post">
                        <div class="header">
                            <h3>March Update</h3>
                            March 14, 2024
                        </div>
                        <div class="content">
                            <p>It hasn't been too long since our last update, but we've already got a bunch of new things to share!</p>
                            <p>
                                BC Transit has started releasing GTFS for many of the new systems we've added over the last year.
                                Unfortunately, they also changed how buses are included in the data feed, so the NIS buses from those systems have disappeared.
                                Luckily, realtime is starting to go live as well - buses from Smithers and other systems are already online, and more should be coming soon!
                            </p>
                            <p>We've also made some big changes and improvements to the website, some of which you may have encountered already, and some of which are getting released along with this news post!</p>
                            <ul>
                                <li>Redesigned and improved the site-wide search bar and results</li>
                                <li>Added support for seeing all systems at once on the routes map page</li>
                                <li>Added date filters and statistics on the vehicle history page</li>
                                <li>Added scheduled bus info to trip pages before they've run</li>
                                <li>Bug fixes and performance improvements behind the scenes</li>
                            </ul>
                            <p>Thank you for continuing to support BCTracker!</p>
                        </div>
                    </div>
                    <div class="news-post">
                        <div class="header">
                            <h3>Change to Maps</h3>
                            January 27, 2024
                        </div>
                        <div class="content">
                            <p>
                                Hi everyone, quick announcement about some changes to the map screens.
                                After Victoria's NextRide website was shut down last week, we've seen some big increases to how much our site is being used (which is great to see - welcome newcomers!!).
                                The downside is the increase in site visits has put us well over the threshold for unpaid MapBox usage, and racked up some not-insignificant fees.
                                As a one-time thing that's not a problem, but we'd rather not be paying double for maps what we pay for the rest of the website hosting every month.
                            </p>
                            <p>
                                As a result, we've decided to change the provider of our maps from MapBox to OpenLayers.
                                If you've used the T-Comm site for Vancouver before this should look familiar - it uses the same OpenStreetMaps source.
                                Overall everything should work more or less the same, with a couple of exceptions:
                            </p>
                            <ul>
                                <li>The appearance of the map is now different, no longer as minimalist and no longer light/dark mode-dependent</li>
                                <li>The geotracker for your current location, which was built-in with MapBox, is no longer available</li>
                            </ul>
                            <p>
                                Down the road as we get more used to this provider we hope to be able to undo those changes to get maps as close to how they used to be as possible.
                                For now we thank you for your patience and understanding!
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
    
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>Community</h2>
            </div>
            <div class="content">
                <p>Join the BCTracker Discord server - a home for transit riders and enthusiasts from around British Columbia!</p>
                <iframe src="https://discord.com/widget?id=925662392053022720&theme=dark" width="100%" height="300px" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
            </div>
        </div>
    </div>
</div>
