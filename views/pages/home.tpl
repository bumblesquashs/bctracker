
% import repositories

% rebase('base')

<div id="page-header">
    <h1>Welcome to BCTracker!</h1>
    % if context.system:
        % if context.realtime_enabled:
            <h2>{{ context }} Transit Schedules and {{ context.vehicle_type }} Tracking</h2>
        % else:
            <h2>{{ context }} Transit Schedules</h2>
        % end
    % else:
        <h2>British Columbia Transit Schedules and {{ context.vehicle_type }} Tracking</h2>
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
                    function vehicleSearch() {
                        let value = document.getElementById('vehicle_search').value;
                        if (value.length > 0) {
                            window.location = "{{ get_url(context, 'bus') }}/" + value;
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
                        <form onsubmit="vehicleSearch()" action="javascript:void(0)">
                            <label for="vehicle_search">{{ context.vehicle_type }} Number or Name:</label>
                            <div class="input-container">
                                <input type="text" id="vehicle_search" name="vehicle_search" method="post" size="10">
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
                    
                    % if context.enable_blocks:
                        <form onsubmit="blockSearch()" action="javascript:void(0)">
                            <label for="block_search">Block ID:</label>
                            <div class="input-container">
                                <input type="text" id="block_search" name="block_search" method="post" size="10">
                                <input type="submit" value="Search" class="button">
                            </div>
                        </form>
                    % end
                % else:
                    <form onsubmit="vehicleSearch()" action="javascript:void(0)">
                        <label for="vehicle_search">{{ context.vehicle_type }} Number or Name:</label>
                        <div class="input-container">
                            <input type="text" id="vehicle_search" name="vehicle_search" method="post" size="10">
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
                    Favourites have been moved to a <a href="{{ get_url(context, 'favourites') }}">dedicated page</a>!
                </p>
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
                            <h3>{{ context.vehicle_type }} Tracking</h3>
                            <p>See all {{ context.vehicle_type_plural.lower() }} that are currently active, including current route and location</p>
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
                            % if context.enable_blocks:
                                <a class="button" href="{{ get_url(context, 'blocks') }}">Blocks</a>
                            % end
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
                            <h3>BCTracker AI Chat</h3>
                            April 1st, 2026
                        </div>
                        <div class="content">
                            <p class="smaller-font lighter-text">Sure, here is a news post for the new AI chat feature written in the style of the BCTracker developers:</p>
                            <p>
                                It's never too late to jump on the bandwagon.
                                BCTracker is finally introducing an AI chat to help you get information faster!
                            </p>
                            <p>
                                For your convenience, the chat is designed to take up a large portion of your screen and there's no way to remove it, so you can't just ignore this amazing new feature.
                                All responses are guaranteed to be 100% correct anyways - you probably won't even need the rest of the website anymore.
                            </p>
                            <p>For more information, please see the AI chat section on the <a href="{{ get_url(context, 'about') }}#ai">About</a> page.</p>
                            <p>We hope you enjoy, and have a safe summer!</p>
                            <p class="smaller-font lighter-text">Let me know if you'd like any modifications or something different.</p>
                            % if today.day != 1 or now.hour >= 12:
                                <i>... Happy April Fools Day!</i>
                            % end
                        </div>
                    </div>
                    <div class="news-post">
                        <div class="header">
                            <h3>Summer Update</h3>
                            July 21st, 2025
                        </div>
                        <div class="content">
                            <p>
                                Let's jump right in with the big news: BCTracker now includes schedule data for <b>BC Ferries</b>!
                                We're still figuring out the best way to integrate realtime data for tracking vessels, so that will be added down the road.
                                In the meantime we hope the schedule information is still useful!
                            </p>
                            <p>
                                As always, there's been a bunch of other improvements since our last update post that you may have noticed already.
                                This includes:
                            </p>
                            <ul>
                                <li>Stop icons on the main map page</li>
                                <li>Geolocation and dark mode for maps</li>
                                <li>Redesigned status bar on desktop</li>
                                <li>Trips with changing headsigns</li>
                                <li>The new <b>West Coast</b> system</li>
                            </ul>
                            <p>We've also been busy making some memory usage improvements to keep the site running smoothly and prepare for larger datasets such as Translink.</p>
                            <p>See you in the next update!</p>
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
