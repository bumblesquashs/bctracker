
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
                <h2>Favourites</h2>
            </div>
            <div class="content">
                <p>
                    Add up to 10 favourites using the
                    % include('components/svg', name='non-favourite')
                    button on buses, routes, and stops.
                </p>
                % if favourites:
                    <table>
                        <thead>
                            <tr>
                                <th>Favourite</th>
                            </tr>
                        </thead>
                        <tbody>
                            % for favourite in favourites:
                                % value = favourite.value
                                <tr>
                                    <td>
                                        <div class="column">
                                            % if favourite.type == 'vehicle':
                                                <a href="{{ get_url(system, f'bus/{value.number}') }}">Bus {{ value }}</a>
                                                <div class="smaller-font">{{! value.order }}</div>
                                            % elif favourite.type == 'route':
                                                <a href="{{ get_url(value.system, f'routes/{value.number}') }}">{{ value.system }} Route {{ value.number }}</a>
                                                <div class="smaller-font">{{! value.display_name }}</div>
                                            % elif favourite.type == 'stop':
                                                <a href="{{ get_url(value.system, f'stops/{value.number}') }}">{{ value.system }} Stop {{ value.number }}</a>
                                                <div class="smaller-font">{{ value.name }}</div>
                                            % end
                                        </div>
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                % end
            </div>
        </div>
    </div>
    
    <div class="container flex-2">
        <div class="section">
            <div class="header">
                <h2>Quick Navigation</h2>
            </div>
            <div class="content">
                <div id="quick-navigation">
                    <div class="item">
                        <div class="column center">
                            % include('components/svg', name='realtime')
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
                            % include('components/svg', name='route')
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
        <div class="section">
            <div class="header">
                <h2>Latest News</h2>
            </div>
            <div class="content">
                <div class="container">
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
                    <div class="news-post">
                        <div class="header">
                            <h3>Winter Update</h3>
                            January 14, 2024
                        </div>
                        <div class="content">
                            <p>
                                Thank you to everyone who has filled out our survey from the last post!
                                Your responses have been very helpful for figuring out what features we should add, and what areas we should focus on for improvement.
                                We'll be working on making those changes over the next while, so keep an eye out!
                            </p>
                            <p>
                                Since our last update we've continued adding features and making improvements to help make the website more useful.
                                The most notable changes include:
                            </p>
                            <ul>
                                <li>Upcoming departures from nearby stops</li>
                                <li>Upcoming stops on bus pages</li>
                                <li>Timelines on block and bus pages</li>
                                <li>Filter for NIS buses on the realtime page</li>
                                <li>Bus icon styles on the personalize page</li>
                                <li>Support for searching block IDs</li>
                                <li>Lots of other fixes and improvements</li>
                            </ul>
                            <p>
                                There's also been a few other events of note since last summer:
                            </p>
                            <ul>
                                <li>
                                    BC Transit has started updating all the old v1 NextRide systems to the newer v2 hardware and software.
                                    This has caused a few inconsistencies with the data during each upgrade, but so far everything has been going smoothly.
                                    As of this post, Victoria is the only system left to go and will start the conversion process this week.
                                </li>
                                <li>
                                    Many new systems have been added, including <b>100 Mile House</b>, <b>Ashcroft-Clinton</b>, <b>Bella Coola</b>,
                                        <b>Clearwater</b>, <b>Merritt</b>, <b>Pemberton</b>, <b>Quesnel</b>, <b>Revelstoke</b>, <b>Salt Spring Island</b>,
                                        <b>Smithers</b>, and <b>Williams Lake</b>.
                                    Additionally, some new smaller systems have been grouped into existing bigger systems.
                                    This includes <b>Boundary</b> as part of West Kootenay, <b>Bulkley-Nechako</b> as part of Prince George, and
                                        <b>Hazeltons</b> as part of Kitimat-Stikine.
                                    Putting it all together, that means we're now supporting 100% of existing BC Transit systems!
                                    At the moment, these newest systems only have realtime data feeds - we expect the static route and schedule information to become available later this year, after the v1 to v2 upgrades are complete.
                                </li>
                                <li>
                                    In late November, our website hosting service went offline and we were forced to quickly migrate to a new host.
                                    Thanks to regular backups and our impeccable programming skills, we were running again soon after with minimal data loss.
                                    Our apologies to anyone who was affected when that was happening!
                                </li>
                                <li>
                                    For a few weeks we found the website was experiencing high numbers of page requests which caused the server to become burdened and eventually crash.
                                    We eventually determined this was coming from scraper bots trying to map out the website.
                                    With pages for every trip getting requested non-stop, it was just too much for the server to handle.
                                    We have since blocked those bots, and apologize again to anyone who was affected when <i>that</i> was happening!
                                </li>
                                <li>
                                    Lastly, following the above two points, we've been putting more effort into some of the internals of the website as well as normal features, to help make it more efficient.
                                    As a result, the website now uses less memory and reboots much faster if issues do occur.
                                    If you notice any strange behaviour or broken stuff, please let us know!
                                </li>
                            </ul>
                            <p>
                                Well, this is definitely the longest news post we've made yet - if you've gotten here, thanks for sticking with it!
                                We're going to try post more frequent updates here to keep things short and sweet in the future.
                            </p>
                            <p>
                                TL;DR - we've added some cool stuff and we're looking forward to adding more cool stuff!
                                Happy New Year to everyone and, as always, stay safe out there!
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
