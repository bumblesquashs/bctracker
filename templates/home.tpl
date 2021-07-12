% rebase('base', title='Home' if system is None else 'BCTracker')

<h1>
  % if system is None:
    Welcome to BCTracker!
  % else:
    Welcome to BCTracker {{ system }}!
  % end
</h1>
<hr />

<div class="sidebar">
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
        window.location = "{{ get_url(system) }}/stops/" + value;
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
      <label for="stop_id_search">Stop Number:</label>
      <br />
      <input type="text" id="stop_id_search" name="stop_id" method="post">
      <input type="submit" value="Search" class="button">
    </form>
  % end

  % if system is None:
    <p>Choose a system to search for routes and stops</p>
    % include('components/systems')
  % end
</div>

<div class="body">
  <h2>Latest Updates</h2>

  <div class="news-post">
    <div class="news-post-header">
      <h3>More Transit Systems</h3>
      July 12, 2021
    </div>
    <div class="news-post-content">
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
      Have a great summer!
    </div>
  </div>
  <div class="news-post">
    <div class="news-post-header">
      <h3>New Deckers Out!</h3>
      April 1, 2021
    </div>
    <div class="news-post-content">
      <p>
        BCTracker has been updated to support the latest deckers, which have just entered service.
      </p>
      Stay safe everyone!
    </div>
  </div>
  <div class="news-post-older">
    <a href="{{ get_url(system, 'news') }}">See older updates</a>
  </div>
</div>
