
% import repositories

% rebase('base')

<div id="page-header">
    <h1>Welcome to ABTracker!</h1>
    % if context.system:
        % if context.realtime_enabled:
            <h2>{{ context }} Transit Schedules and Bus Tracking</h2>
        % else:
            <h2>{{ context }} Transit Schedules</h2>
        % end
    % else:
        <h2>Alberta Transit Schedules and Bus Tracking</h2>
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
                    <p>Choose an agency to search for routes and stops</p>
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
                                                    % position = repositories.position.find(value)
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
                                            % favourite_systems = {f.value.context.system for f in route_favourites}
                                            % for system in sorted(favourite_systems):
                                                % system_favourites = [f for f in route_favourites if f.value.context.system == system]
                                                <tr class="header">
                                                    <td>{{ system }}</td>
                                                </tr>
                                                <tr class="display-none"></tr>
                                                % for favourite in system_favourites:
                                                    % value = favourite.value
                                                    <tr>
                                                        <td>
                                                            <div class="row">
                                                                % include('components/route', route=value, include_link=False)
                                                                <a href="{{ get_url(value.context, 'routes', value) }}">{{! value.display_name }}</a>
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
                                            % favourite_systems = {f.value.context.system for f in stop_favourites}
                                            % for system in sorted(favourite_systems):
                                                % system_favourites = [f for f in stop_favourites if f.value.context.system == system]
                                                <tr class="header">
                                                    <td colspan="2">{{ system }}</td>
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
                    <div class="news-post">
                        <div class="header">
                            <h3>Welcome to ABTracker!</h3>
                            April 1st, 2025
                        </div>
                        <div class="content">
                            <p>
                                ABTracker is a new spinoff from <a href="https://bctracker.ca">BCTracker</a> for folks living in Alberta!
                                We hope you find it useful for tracking down your buses.
                                Then again Alberta is so flat that you can probably just see your bus from wherever you happen to be standing.
                            </p>
                            <p>
                                Originally this website was meant to be a one-day April Fools joke, but there was so much interest in it that we're going to try keeping it around for longer!
                                It turns out we were the fools all along for not anticipating this...
                            </p>
                            <p>
                                For now the website is going to be in <b>beta</b>, which means that some stuff could still break or get changed at any time.
                                Please see the <a href="{{ get_url(context, 'about') }}#beta-testing">about page</a> for more info.
                            </p>
                            <p>
                                Enjoy!
                            </p>
                        </div>
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
                <p>Join the BCTracker Discord server - it's mainly folks in British Columbia but you're welcome too!</p>
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
