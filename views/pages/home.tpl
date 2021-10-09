% rebase('base', title='Home' if system is None else 'BCTracker')

<div class="page-header">
    % if system is None:
        <h1 class="title">Welcome to BCTracker!</h1>
    % else:
        <h1 class="title">Welcome to BCTracker {{ system }}!</h1>
    % end
</div>
<hr />

<div id="sidebar">
    <h2>Quick Search</h2>
    
    <script type="text/javascript">
        function busSearch() {
            let value = document.getElementById('bus_id_search').value;
            if (value.length > 0) {
                window.location = "{{ get_url(system) }}/bus/" + value;
            }
        }
        
        function routeSearch() {
            let value = document.getElementById('route_id_search').value;
            if (value.length > 0) {
                window.location = "{{ get_url(system) }}/routes/" + value;
            }
        }
        
        function stopSearch() {
            let value = document.getElementById('stop_id_search').value;
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
            <label for="bus_id_search">Bus Number:</label>
            <br />
            <input type="text" id="bus_id_search" name="bus_id" method="post">
            <input type="submit" value="Search" class="button">
        </form>
    % else:
        % if system.realtime_enabled:
            <form onsubmit="busSearch()" action="javascript:void(0)">
                <label for="bus_id_search">Bus Number:</label>
                <br />
                <input type="text" id="bus_id_search" name="bus_id" method="post">
                <input type="submit" value="Search" class="button">
            </form>
        % end
        
        <form onsubmit="routeSearch()" action="javascript:void(0)">
            <label for="route_id_search">Route Number:</label>
            <br />
            <input type="text" id="route_id_search" name="route_id" method="post">
            <input type="submit" value="Search" class="button">
        </form>
        
        <form onsubmit="stopSearch()" action="javascript:void(0)">
            <label for="stop_id_search">Stop Number or Name:</label>
            <br />
            <input type="text" id="stop_id_search" name="stop_id" method="post">
            <input type="submit" value="Search" class="button">
        </form>
    % end
    
    % if system is None:
        <p>Choose a system to search for routes and stops</p>
        % include('components/systems')
    % end
    
    <div class="theme-control">
        <h2>Theme</h2>
        <div>
            <a class="button" href="?theme=automatic">Automatic</a>
            <a class="button" href="?theme=light">Light</a>
            <a class="button" href="?theme=dark">Dark</a>
            <!-- Oh, hello there! Green and white is nice, but I wonder what the site would look like in "classic" colours. If only there was a way to set the theme to "classic"... -->
        </div>
    </div>
</div>

<div>
    <h2>Latest Updates</h2>
    
    <div class="news-post">
        <div class="header">
            <h3>Fall Update</h3>
            September 21, 2021
        </div>
        <div class="content">
            <p>
                Over the last couple months you may have noticed some exciting new features appearing around the website.
                We're trying to keep updates more frequent, rather than releasing massive changes once or twice per year.
            </p>
            <p>
                Since the big multi-system update earlier this summer, we've introduced:
            </p>
            <ul>
                <li>Schedule Adherence: How many minutes ahead or behind schedule a bus is (approximately)</li>
                <li>Nearby Stops: Easy transfers that are within 100m of the stop you're looking at</li>
                <li>Dark Theme: Can be set automatically based on your device's current preferences, or set manually</li>
                <li>Tablet Layouts: Specially designed for screens bigger than a phone but smaller than a computer</li>
                <li>Lots more minor improvements and fixes behind the scenes</li>
            </ul>
            <p>
                We appreciate your feedback, and we're looking forward to turning more of your suggestions into new features and improvements.
                Stay tuned for more this fall!
            </p>
        </div>
    </div>
    <div class="news-post">
        <div class="header">
            <h3>More Transit Systems</h3>
            July 12, 2021
        </div>
        <div class="content">
            <p>
                You asked for it, and we listened!
                That's right, BCTracker now supports multiple transit systems across British Columbia.
            </p>
            <p>
                We're starting with 10 cities and regions from around the province, and we plan to add more in the future.
                These initial systems include all seven currently enabled with realtime information, as well as three that only provide schedule data.
                You can easily swap between these systems at any time using the dropdown at the top right corner of your screen.
            </p>
            <p>
                In addition to all the new transit systems, we've also made a bunch of improvements to the general website design.
                System-wide realtime maps, route maps and information panels, improved desktop layouts, and many more useful features are now available!
            </p>
            <p>
                There's always more to do, and your feedback helps us figure out what comes next.
                You can send an email to <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know what you like and what can be made better.
            </p>
            <p>
                Have a great summer!
            </p>
        </div>
    </div>
    <div class="news-post-older">
        <a href="{{ get_url(system, 'news') }}">See older updates</a>
    </div>
</div>
