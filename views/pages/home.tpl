
% rebase('base')

<div id="page-header">
    <h1>Welcome to ABTracker!</h1>
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
        <h2>Alberta Transit Schedules and {{ context.vehicle_type }} Tracking</h2>
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
                            window.location = getURL(currentAgencyID, currentSystemID, "fleet/" + value);
                        }
                    }
                    
                    function routeSearch() {
                        let value = document.getElementById('route_search').value;
                        if (value.length > 0) {
                            window.location = getURL(currentAgencyID, currentSystemID, "routes/" + value);
                        }
                    }
                    
                    function stopSearch() {
                        let value = document.getElementById('stop_search').value;
                        if (value.length > 0) {
                            if (isNaN(value)) {
                                window.location = getURL(currentAgencyID, currentSystemID, "stops", false, {
                                    "search": value
                                });
                            } else {
                                window.location = getURL(currentAgencyID, currentSystemID, "stops/" + value);
                            }
                        }
                    }
                    
                    function blockSearch() {
                        let value = document.getElementById('block_search').value;
                        if (value.length > 0) {
                            window.location = getURL(currentAgencyID, currentSystemID, "blocks/" + value);
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
                                Please see the <a href="{{ context.url('about') }}#beta-testing">about page</a> for more info.
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
