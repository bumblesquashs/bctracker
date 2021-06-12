<html>
  <head> 
    <title>BCTracker | {{ title }}</title>

    <link rel="icon" type="image/png" href="/img/busicon.png"/>

    % supports_realtime = defined('system') and system.supports_realtime
    
    <!-- prevent this website from being searchable -->
    <meta name="robots" content="noindex" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />

    <link rel="stylesheet" href="/style/main.css" />
    <link rel="stylesheet" media="screen and (min-width: 768px)" href="/style/main-desktop.css" />
    <link rel="stylesheet" media="screen and (max-width: 767px)" href="/style/main-mobile.css" />
    <link rel="stylesheet" href="/style/tables.css" />
    
    % if defined("include_maps") and include_maps:
      <script src='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.js'></script>
      <link href='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.css' rel='stylesheet' />
    % end
  </head>
  
  <body>
    <script>
      var showMobileNavbar = false;

      function toggleMobileNavbar() {
        const element = document.getElementById("mobile-navbar")
        if (showMobileNavbar) {
          showMobileNavbar = false;
          element.className = "mobile-only display-none"
        } else {
          showMobileNavbar = true;
          element.className = "mobile-only"
        }
      }
    </script>
    <div id="navbar">
      <a class="navbar-item navbar-title" href="/">BCTracker</a>

      <div class="desktop-only">
        % if supports_realtime:
          <a class="navbar-item" href="/realtime">Realtime</a>
        % end
        <a class="navbar-item" href="/routes">All Routes</a>
        <a class="navbar-item" href="/blocks">All Blocks</a>
        % if supports_realtime:
          <a class="navbar-item" href="/history">Vehicle History</a>
        % end
        <a class="navbar-item" href="/about">About</a>
        % if defined('system'):
          <div class="navbar-item navbar-right dropdown">
            {{ system }}
            <div class="dropdown-content">
              <div class="dropdown-title">Change System</div>
              % for available_system in sorted(systems):
                % if system != available_system:
                  <a href="http://{{ available_system.system_id }}.bctracker.ca">{{ available_system }}</a>
                % end
              % end
            </div>
          </div>
        % end
      </div>

      <div class="mobile-navbar-toggle mobile-only" onclick="toggleMobileNavbar()">
        <div class="mobile-navbar-toggle-line"></div>
        <div class="mobile-navbar-toggle-line"></div>
        <div class="mobile-navbar-toggle-line"></div>
      </div>
      <br style="clear: both" />
    </div>
    
    <div id="mobile-navbar" class="mobile-only display-none">
      % if supports_realtime:
        <a class="mobile-navbar-item" href="/realtime">Realtime</a>
      % end
      <a class="mobile-navbar-item" href="/routes">All Routes</a>
      <a class="mobile-navbar-item" href="/blocks">All Blocks</a>
      % if supports_realtime:
        <a class="mobile-navbar-item" href="/history">Vehicle History</a>
      % end
      <a class="mobile-navbar-item" href="/about">About</a>
      % if defined('system'):
        <a class="mobile-navbar-item" href="/">{{ system }}</a>
      % end
    </div>
    
    <div id="content">
      {{ !base }}
    </div>
  </body>
</html>