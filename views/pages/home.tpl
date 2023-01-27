
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
    <div class="sidebar container flex-1">
        <div>
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
        </div>
        <div>
            <h2>Community</h2>
            <p>
                Join the BCTracker Discord server - a home for transit riders and enthusiasts from around British Columbia!
            </p>
            <iframe src="https://discord.com/widget?id=925662392053022720&theme=dark" width="100%" height="300px" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
        </div>
    </div>
    
    <div class="container flex-3">
        <div>
            <h2>Latest Updates</h2>
            <div class="container">
                <div class="news-post">
                    <div class="header">
                        <h3>Winter Update</h3>
                        December 8, 2022
                    </div>
                    <div class="content">
                        <p>
                            Starting today, we're introducing a new way to see what days of the week routes, stops, blocks, and trips have normal service, and what dates have modified or no service.
                            Along with providing a handy overview, the new design works as links to go directly to the detailed schedule view.
                            This is a big step forward in our quest to make BC Transit's schedules easy to understand - despite their apparent efforts to make it as complex as possible!
                        </p>
                        <p>
                            A few other small updates have also made their way onto the website, including:
                        </p>
                        <ul>
                            <li>Total number of routes/stops/blocks is shown per system when looking at all systems</li>
                            <li>Toggle for NIS buses on the main map</li>
                            <li>A new high contrast accessibility theme for people who are visually impaired</li>
                        </ul>
                        <p>
                            As always, feedback on the latest changes is welcome and appreciated.
                            Enjoy the holidays and stay safe out there!
                        </p>
                    </div>
                </div>
                <div class="news-post">
                    <div class="header">
                        <h3>Summer Update</h3>
                        August 29, 2022
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
                            Even if you don't have any feedback, everyone is welcome to come chat, share photos and videos, and more.
                            With the BCTracker Bot, you can get alerted when new buses enter service or transfer between systems.
                            And if you enjoy transit photography, we're also kicking it off with a back-to-school photo contest with special Discord roles for the winners!
                        </p>
                        <p>
                            That's all for now - enjoy the rest of the summer!
                        </p>
                    </div>
                </div>
                <div>
                    <a href="{{ get_url(system, 'news') }}">See older updates</a>
                </div>
            </div>
        </div>
    </div>
</div>
