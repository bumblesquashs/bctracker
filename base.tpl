<html>
  <head> 
    <title>
      % if defined('system'):
        {{ system }} | {{ title }}
      % else:
        BCTracker | {{ title }}
      % end
    </title>

    <link rel="icon" type="image/png" href="/img/busicon.png"/>
    
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
      % if defined('system'):
        <a class="navbar-item navbar-title" href="{{ get_url(system.id) }}">BCTracker - {{ system }}</a>
      % else:
        <a class="navbar-item navbar-title" href="{{ get_url('victoria') }}">BCTracker</a>
      % end

      % if defined('system'):
        <div class="desktop-only">
          % if system.supports_realtime:
            <a class="navbar-item" href="{{ get_url(system.id, 'realtime') }}">Realtime</a>
          % end
          <a class="navbar-item" href="{{ get_url(system.id, 'routes') }}">Routes</a>
          <a class="navbar-item" href="{{ get_url(system.id, 'blocks') }}">Blocks</a>
          % if system.supports_realtime:
            <a class="navbar-item" href="{{ get_url(system.id, 'history') }}">History</a>
          % end
          <a class="navbar-item" href="{{ get_url(system.id, 'about') }}">About</a>
          <div class="navbar-item navbar-right dropdown">
            Change System
            <div class="dropdown-content">
              % for available_system in sorted(systems):
                % if system != available_system:
                  <a href="{{ get_url(available_system.id) }}">{{ available_system }}</a>
                % end
              % end
            </div>
          </div>
        </div>

        <div class="mobile-navbar-toggle mobile-only" onclick="toggleMobileNavbar()">
          <div class="mobile-navbar-toggle-line"></div>
          <div class="mobile-navbar-toggle-line"></div>
          <div class="mobile-navbar-toggle-line"></div>
        </div>
      % end
      <br style="clear: both" />
    </div>
    
    % if defined('system'):
      <div id="mobile-navbar" class="mobile-only display-none">
        % if system.supports_realtime:
          <a class="mobile-navbar-item" href="{{ get_url(system.id, 'realtime') }}">Realtime</a>
        % end
        <a class="mobile-navbar-item" href="{{ get_url(system.id, 'routes') }}">Routes</a>
        <a class="mobile-navbar-item" href="{{ get_url(system.id, 'blocks') }}">Blocks</a>
        % if system.supports_realtime:
          <a class="mobile-navbar-item" href="{{ get_url(system.id, 'history') }}">History</a>
        % end
        <a class="mobile-navbar-item" href="{{ get_url(system.id, 'about') }}">About</a>
      </div>
    % end
    
    <div id="content">
      {{ !base }}
    </div>
  </body>
</html>