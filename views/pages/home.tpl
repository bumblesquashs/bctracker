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
            <br />
            <input type="text" id="bus_search" name="bus_search" method="post">
            <input type="submit" value="Search" class="button">
        </form>
    % else:
        % if system.realtime_enabled:
            <form onsubmit="busSearch()" action="javascript:void(0)">
                <label for="bus_search">Bus Number:</label>
                <br />
                <input type="text" id="bus_search" name="bus_search" method="post">
                <input type="submit" value="Search" class="button">
            </form>
        % end
        
        <form onsubmit="routeSearch()" action="javascript:void(0)">
            <label for="route_search">Route Number:</label>
            <br />
            <input type="text" id="route_search" name="route_search" method="post">
            <input type="submit" value="Search" class="button">
        </form>
        
        <form onsubmit="stopSearch()" action="javascript:void(0)">
            <label for="stop_search">Stop Number or Name:</label>
            <br />
            <input type="text" id="stop_search" name="stop_search" method="post">
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
    
    <div class="news-post" id="survey">
        <div class="header">
            <h3>BCTracker Survey</h3>
            November 28, 2021
        </div>
        <div class="content">
            <p>
                We're running a quick survey over the next few weeks to get a better sense of who is using BCTracker, and for what purpose.
                This information will help us understand what new features should have the highest priority, as well as what improvements can be made to existing features.
                It's also a great opportunity for you to give us general feedback about things you like and things you think could be better.
            </p>
            <p>
                If you have a couple spare minutes, we would very much appreciate hearing from you.
                Thanks for supporting BCTracker!
            </p>
            <p>
                <button class="button survey-button" onclick="openSurvey()">Take the survey!</button>
            </p>
        </div>
    </div>
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
    <div class="news-post-older">
        <a href="{{ get_url(system, 'news') }}">See older updates</a>
    </div>
</div>
