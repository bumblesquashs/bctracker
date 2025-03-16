
% from repositories import PositionRepository

% rebase('base')

<div id="page-header">
    <h1>Welcome to BCTracker!</h1>
    % if context.system:
        % if context.realtime_enabled:
            <h2>{{ context.system }} Transit Schedules and Bus Tracking</h2>
        % else:
            <h2>{{ context.system }} Transit Schedules</h2>
        % end
    % else:
        <h2>British Columbia Transit Schedules and Bus Tracking</h2>
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
                                window.location = "{{ get_url(context, 'bus') }}/" + value;
                            }
                        }
                    }
                    
                    function routeSearch() {
                        let value = document.getElementById('route_search').value;
                        if (value.length > 0) {
                            window.location = "{{ get_url(context, 'routes') }}/" + value;
                        }
                    }
                    
                    function stopSearch() {
                        let value = document.getElementById('stop_search').value;
                        if (value.length > 0) {
                            if (isNaN(value)) {
                                window.location = "{{ get_url(context, 'stops') }}?search=" + value;
                            } else {
                                window.location = "{{ get_url(context, 'stops') }}/" + value;
                            }
                        }
                    }
                    
                    function blockSearch() {
                        let value = document.getElementById('block_search').value;
                        if (value.length > 0) {
                            window.location = "{{ get_url(context, 'blocks') }}/" + value;
                        }
                    }
                </script>
                
                % if context.system:
                    % if context.realtime_enabled:
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
                    % include('components/svg', name='action/non-favourite')
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
                                                                    <div class="row gap-5">
                                                                        % include('components/occupancy', occupancy=position.occupancy, show_tooltip=True)
                                                                        % include('components/adherence', adherence=position.adherence)
                                                                    </div>
                                                                % end
                                                            </div>
                                                        </td>
                                                        <td>
                                                            % if position and position.trip:
                                                                % include('components/headsign', departure=position.departure, trip=position.trip)
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
                                                                <a href="{{ get_url(value.system, 'routes', value) }}">{{! value.display_name }}</a>
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
                                                <th>Stop</th>
                                                <th>Routes</th>
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
                                                            % include('components/stop', stop=value)
                                                        </td>
                                                        <td>
                                                            % include('components/route_list', routes=value.routes)
                                                        </td>
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
                            <a class="button" href="{{ get_url(context, 'realtime') }}">List</a>
                            <a class="button" href="{{ get_url(context, 'map') }}">Map</a>
                            <a class="button" href="{{ get_url(context, 'history') }}">History</a>
                        </div>
                    </div>
                    <div class="item">
                        <div class="column center">
                            % include('components/svg', name='route')
                            <h3>Schedules and Maps</h3>
                            <p>See departure times and routing details for routes, stops, blocks, and more</p>
                        </div>
                        <div class="button-container">
                            <a class="button" href="{{ get_url(context, 'routes') }}">Routes</a>
                            <a class="button" href="{{ get_url(context, 'stops') }}">Stops</a>
                            <a class="button" href="{{ get_url(context, 'blocks') }}">Blocks</a>
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
                    <div class="news-post" id="abtracker">
                        <div class="header">
                            <h3>Introducing ABTracker</h3>
                            April 1, 2025
                        </div>
                        <div class="content">
                            <p>
                                Following the great success of BCTracker, we've decided it's time to expand to new territory.
                                The most obvious choice of course is our neighbours to the east, so without further ado we're very pleased to announce the launch of <b><a href="https://abtracker.ca">ABTracker</a></b>!
                            </p>
                            <p>
                                Like BCTracker, ABTracker pulls together transit data from a bunch of larger communities in Alberta into one place, making it easy to see buses running all over the province.
                                The following agencies/systems are supported as of this initial launch:
                            </p>
                            <ul>
                                <li>Calgary Transit (Calgary)</li>
                                <li>Edmonton Transit Service (Edmonton)</li>
                                <li>Grande Prairie Transit (Grande Prairie)</li>
                                <li>Lethbridge Transit (Lethbridge) <i>(no realtime)</i></li>
                                <li>Medicine Hat Transit (Medicine Hat)</li>
                                <li>Red Deer Transit (Red Deer) <i>(no realtime)</i></li>
                                <li>Roam (Banff)</li>
                                <li>Woosh (Fort McMurray)</li>
                            </ul>
                            <p>
                                We hope you find ABTracker useful as we all inevitably move to Alberta for cheaper housing!
                            </p>
                            <p><b>UPDATE:</b></p>
                            <p>
                                So, despite intending for this to be a one-day April Fools joke, a lot of people really want ABTracker permanently!
                                It turns out we were the fools all along for not anticipating this...
                            </p>
                            <p>
                                Instead of taking down the website at the end of the day, we're instead going to leave it available but advertised as being in <b>beta</b>, which means that some stuff could still break or get changed at any time.
                                Please see the <a href="https://abtracker.ca/about#beta-testing">ABTracker about page</a> for more info.
                            </p>
                        </div>
                    </div>
                    <div class="news-post">
                        <div class="header">
                            <h3>Winter Update</h3>
                            January 10th, 2025
                        </div>
                        <div class="content">
                            <p>
                                Happy new year!
                                We're kicking things off with a very exciting announcement: BCTracker is adding support for more transit agencies in BC!
                            </p>
                            <p>
                                We imagine that the first question coming to many minds is "Do you now support TransLink"?
                                The answer is <i>not yet</i>, but hopefully we can get there in the future.
                                For now we're starting with a few small agencies without realtime tracking, to ease ourselves in and have time to iron out any issues before taking on something bigger.
                                The initial new systems/agencies are:
                            </p>
                            <ul>
                                <li><b>Denman Island</b> - operated by <a href="https://www.denmanislandbus.ca">Denman Island Bus</a></li>
                                <li><b>Gabriola Island</b> - operated by <a href="https://gertie.ca">GERTIE</a></li>
                                <li><b>Hornby Island</b> - operated by <a href="https://hornbybus.com">Hornby Bus</a></li>
                            </ul>
                            <p>If you happen to live in or visit one of these places, we hope you find BCTracker useful!</p>
                            <p>In other news, plenty of other improvements have been made since our previous post, including:</p>
                            <ul>
                                <li>Bus occupancy status</li>
                                <li>Time since each bus position was last updated</li>
                                <li>Stop list filtering and sorting</li>
                                <li>Various layout and style updates</li>
                            </ul>
                            <p>Enjoy, stay safe, and have a great year!</p>
                        </div>
                    </div>
                    <div>
                        <a href="{{ get_url(context, 'news') }}">See older news</a>
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
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Support</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <p>We would be incredibly grateful to anyone willing to chip in a little bit to help cover our server and website hosting costs.</p>
                <p>
                    Please, only donate if you can afford to!
                    There is no obligation to do so, and our website will continue to be free to use for all who find it useful or interesting.
                </p>
                <a class="button" target="_blank" href="https://ko-fi.com/bctracker">Donate ❤️</a>
            </div>
        </div>
    </div>
</div>
