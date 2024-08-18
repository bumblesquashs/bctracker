
% from repositories import PositionRepository

% rebase('base')

<div id="page-header">
    <h1>Welcome to BCTracker!</h1>
    % if system:
        <h2>{{ system }} Transit Schedules and Bus Tracking</h2>
    % else:
        <h2>BC Transit Schedules and Bus Tracking</h2>
    % end
</div>

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Quick Search</h2>
                % include('components/toggle')
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
                
                % if system:
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
                % else:
                    <form onsubmit="busSearch()" action="javascript:void(0)">
                        <label for="bus_search">Bus Number:</label>
                        <div class="input-container">
                            <input type="text" id="bus_search" name="bus_search" method="post" size="10">
                            <input type="submit" value="Search" class="button">
                        </div>
                    </form>
                    <p>Choose a system to search for routes and stops</p>
                % end
            </div>
        </div>
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Favourites</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <p>
                    Add up to 20 favourites using the
                    % include('components/svg', name='non-favourite')
                    button on buses, routes, and stops.
                </p>
                % if favourites:
                    % vehicle_favourites = [f for f in favourites if f.type == 'vehicle']
                    % route_favourites = [f for f in favourites if f.type == 'route']
                    % stop_favourites = [f for f in favourites if f.type == 'stop']
                    <div class="container">
                        % if vehicle_favourites:
                            <div class="section">
                                <div class="content">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Bus</th>
                                                <th>Headsign</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % orders = {f.value.order for f in vehicle_favourites}
                                            % for order in sorted(orders):
                                                % order_favourites = [f for f in vehicle_favourites if f.value.order == order]
                                                <tr class="header">
                                                    <td colspan="2">{{! order }}</td>
                                                </tr>
                                                <tr class="display-none"></tr>
                                                % for favourite in order_favourites:
                                                    % value = favourite.value
                                                    % position = di[PositionRepository].find(value)
                                                    <tr>
                                                        <td>
                                                            <div class="row">
                                                                % include('components/bus', bus=value)
                                                                % if position:
                                                                    % include('components/adherence', adherence=position.adherence)
                                                                % end
                                                            </div>
                                                        </td>
                                                        <td>
                                                            % if position and position.trip:
                                                                % include('components/headsign', trip=position.trip)
                                                            % else:
                                                                <div class="lighter-text">Not in service</div>
                                                            % end
                                                        </td>
                                                    </tr>
                                                % end
                                            % end
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        % end
                        % if route_favourites:
                            <div class="section">
                                <div class="content">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Route</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % favourite_systems = {f.value.system for f in route_favourites}
                                            % for favourite_system in sorted(favourite_systems):
                                                % system_favourites = [f for f in route_favourites if f.value.system == favourite_system]
                                                <tr class="header">
                                                    <td>{{ favourite_system }}</td>
                                                </tr>
                                                <tr class="display-none"></tr>
                                                % for favourite in system_favourites:
                                                    % value = favourite.value
                                                    <tr>
                                                        <td>
                                                            <div class="row">
                                                                % include('components/route', route=value, include_link=False)
                                                                <a href="{{ get_url(value.system, f'routes/{value.number}') }}">{{! value.display_name }}</a>
                                                            </div>
                                                        </td>
                                                    </tr>
                                                % end
                                            % end
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        % end
                        % if stop_favourites:
                            <div class="section">
                                <div class="content">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Stop Number</th>
                                                <th>Stop Name</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % favourite_systems = {f.value.system for f in stop_favourites}
                                            % for favourite_system in sorted(favourite_systems):
                                                % system_favourites = [f for f in stop_favourites if f.value.system == favourite_system]
                                                <tr class="header">
                                                    <td colspan="2">{{ favourite_system }}</td>
                                                </tr>
                                                <tr class="display-none"></tr>
                                                % for favourite in system_favourites:
                                                    % value = favourite.value
                                                    <tr>
                                                        <td>
                                                            <a href="{{ get_url(value.system, f'stops/{value.number}') }}">{{ value.number }}</a>
                                                        </td>
                                                        <td>{{ value.name }}</td>
                                                    </tr>
                                                % end
                                            % end
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        % end
                    </div>
                % end
            </div>
        </div>
    </div>
    
    <div class="container flex-2">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Quick Navigation</h2>
                % include('components/toggle')
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
            <div class="header" onclick="toggleSection(this)">
                <h2>Latest News</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="container">
                    <div class="news-post">
                        <div class="header">
                            <h3>Summer Update</h3>
                            June 27, 2024
                        </div>
                        <div class="content">
                            <p>
                                It's summer already - time sure flies!
                                Here's what we've been up to since the last post.
                            </p>
                            <ul>
                                <li>Favourites: A quick way to get to your frequently-used pages from the home page</li>
                                <li>Themes: A new Pride theme, and improvements for High Contrast mode</li>
                                <li>Bus History: Now has paging to improve loading time</li>
                                <li>Mobile Sections: Now can be toggled to make it easier to scroll down</li>
                                <li>Transfers: Now can be filtered and shows statistics</li>
                            </ul>
                            <p>As usual we've also been making small improvements to the general design of the site, as well as improvements to the server itself behind the scenes.</p>
                            <p>On BC Transit's end, we've started seeing more buses in service in some of the new NextRide systems, including <b>Quesnel</b>, <b>Williams Lake</b>, <b>100 Mile House</b>, and <b>Pemberton</b>.</p>
                            <p>
                                That's all from us for now!
                                As always, we appreciate your support and feedback, so let us know if you have any comments or suggestions.
                                Have a great summer!
                            </p>
                        </div>
                    </div>
                    <div class="news-post">
                        <div class="header">
                            <h3>Spring Update</h3>
                            March 30, 2024
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
                    <div>
                        <a href="{{ get_url(system, 'news') }}">See older news</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Community</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <p>Join the BCTracker Discord server - a home for transit riders and enthusiasts from around British Columbia!</p>
                <iframe src="https://discord.com/widget?id=925662392053022720&theme=dark" width="100%" height="300px" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
            </div>
        </div>
    </div>
</div>
