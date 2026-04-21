
% import repositories

% rebase('base')

<div id="page-header">
    <h1>Welcome to BCTracker!</h1>
    % if context.system:
        <div class="row">
            % if context.realtime_enabled:
                <h2>{{ context }} Transit Schedules and {{ context.vehicle_type }} Tracking</h2>
            % else:
                <h2>{{ context }} Transit Schedules</h2>
            % end
            % if len(favourite_system_ids) >= 5 and context.system_id not in favourite_system_ids:
                <div class="favourite disabled tooltip-anchor">
                    % include('components/svg', name='action/non-favourite')
                    <div class="tooltip right">You can only have 5 favourite systems at a time</div>
                </div>
            % else:
                % new_favourite_systems = set(favourite_system_ids)
                % if context.system_id in favourite_system_ids:
                    <div class="favourite tooltip-anchor" onclick="updateFavouriteSystems()">
                        % include('components/svg', name='action/favourite')
                        <div class="tooltip right">Remove favourite system</div>
                    </div>
                    % new_favourite_systems.remove(context.system_id)
                % else:
                    <div class="favourite tooltip-anchor" onclick="updateFavouriteSystems()">
                        % include('components/svg', name='action/non-favourite')
                        <div class="tooltip right">Add favourite system</div>
                    </div>
                    % new_favourite_systems.add(context.system_id)
                % end
                % new_favourite_systems_string = ','.join(sorted(new_favourite_systems))
                <script>
                    function updateFavouriteSystems() {
                        window.location = "?favourite_systems={{ new_favourite_systems_string }}";
                    }
                </script>
            % end
        </div>
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
                            window.location = "{{ context.url('bus') }}/" + value;
                        }
                    }
                    
                    function routeSearch() {
                        let value = document.getElementById('route_search').value;
                        if (value.length > 0) {
                            window.location = "{{ context.url('routes') }}/" + value;
                        }
                    }
                    
                    function stopSearch() {
                        let value = document.getElementById('stop_search').value;
                        if (value.length > 0) {
                            if (isNaN(value)) {
                                window.location = "{{ context.url('stops') }}?search=" + value;
                            } else {
                                window.location = "{{ context.url('stops') }}/" + value;
                            }
                        }
                    }
                    
                    function blockSearch() {
                        let value = document.getElementById('block_search').value;
                        if (value.length > 0) {
                            window.location = "{{ context.url('blocks') }}/" + value;
                        }
                    }
                </script>
                
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
            </div>
        </div>
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Favourites</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <p>
                    Favourites have been moved to a <a href="{{ context.url('favourites') }}">dedicated page</a> with more details!
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
                            <a class="button" href="{{ context.url('realtime') }}">List</a>
                            <a class="button" href="{{ context.url('map') }}">Map</a>
                            <a class="button" href="{{ context.url('history') }}">History</a>
                        </div>
                    </div>
                    <div class="item">
                        <div class="column center">
                            % include('components/svg', name='route')
                            <h3>Schedules and Maps</h3>
                            <p>See departure times and routing details for routes, stops, blocks, and more</p>
                        </div>
                        <div class="button-container">
                            <a class="button" href="{{ context.url('routes') }}">Routes</a>
                            <a class="button" href="{{ context.url('stops') }}">Stops</a>
                            % if context.enable_blocks:
                                <a class="button" href="{{ context.url('blocks') }}">Blocks</a>
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
                            <h3>Spring Update</h3>
                            April 13th, 2026
                        </div>
                        <div class="content">
                            <p>
                                Long time no post!
                                We've made a few improvements to favourites on the site.
                            </p>
                            <ul>
                                <li>You can now add favourite systems, which are shown at the top of the systems list</li>
                                <li>
                                    Favourite buses, routes, and stops now have a <a href="{{ context.url('favourites') }}">dedicated page</a>
                                    <ul>
                                        <li>On desktop this can be accessed via the star icon in the navigation bar, on mobile it can be found in the navigation menu</li>
                                    </ul>
                                </li>
                                <li>With more room to show favourites, you can now easily see bus history, active buses on routes, and upcoming departures from stops</li>
                            </ul>
                            <p>
                                We've also made some improvements to searching across all transit systems.
                                Routes, stops, and blocks can be searched at any time.
                                With the quick search, if there's more than one result, you'll be prompted to choose the one you're looking for.
                            </p>
                            <p>As always, thank you for choosing BCTracker!</p>
                        </div>
                    </div>
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
                                All responses are guaranteed to be 100% correct anyways — you probably won't even need the rest of the website anymore.
                            </p>
                            <p>For more information, please see the AI chat section on the <a href="{{ context.url('about') }}#ai">About</a> page.</p>
                            <p>We hope you enjoy, and have a safe summer!</p>
                            <p class="smaller-font lighter-text">Let me know if you'd like any modifications or something different.</p>
                            <i>... Happy April Fools Day!</i>
                        </div>
                    </div>
                    <div>
                        <a href="{{ context.url('news') }}">See older news</a>
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
