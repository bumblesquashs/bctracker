<html>
  <head> 
    <title>
      % if system is None:
        BCTracker | {{ title }}
      % else:
        {{ system }} | {{ title }}
      % end
    </title>

    <link rel="icon" type="image/png" href="/img/favicon.png"/>
    
    <!-- prevent this website from being searchable -->
    <meta name="robots" content="noindex" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />

    <link rel="stylesheet" href="/style/main.css" />
    <link rel="stylesheet" media="screen and (min-width: 803px)" href="/style/main-desktop.css" />
    <link rel="stylesheet" media="screen and (max-width: 802px)" href="/style/main-mobile.css" />
    <link rel="stylesheet" href="/style/tables.css" />
    
    % if defined("include_maps") and include_maps:
      <script src='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.js'></script>
      <link href='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.css' rel='stylesheet' />
    % end

    <script>
      var showMobileNavbar = false;
      function toggleMobileNavbar() {
        const element = document.getElementById("mobile-navbar")
        showMobileNavbar = !showMobileNavbar
        if (showMobileNavbar) {
          element.className = "mobile-only"
        } else {
          element.className = "mobile-only display-none"
        }
      }
    </script>
  </head>
  
  <body>
    <div id="navbar">
      <a class="navbar-item navbar-title" href="{{ get_url(system) }}">BCTracker</a>

      <div class="desktop-only">
        % if system is None:
          <a class="navbar-item" href="{{ get_url(None, 'map') }}">Map</a>
          <a class="navbar-item" href="{{ get_url(None, 'realtime') }}">Realtime</a>
          <a class="navbar-item" href="{{ get_url(None, 'history') }}">History</a>
          <a class="navbar-item" href="{{ get_url(None, 'routes') }}">Routes</a>
          <a class="navbar-item" href="{{ get_url(None, 'blocks') }}">Blocks</a>
          <a class="navbar-item" href="{{ get_url(None, 'about') }}">About</a>
        % else:
          % if system.supports_realtime:
            <a class="navbar-item" href="{{ get_url(system, 'map') }}">Map</a>
            <a class="navbar-item" href="{{ get_url(system, 'realtime') }}">Realtime</a>
            <a class="navbar-item" href="{{ get_url(system, 'history') }}">History</a>
          % else:
            <span class="navbar-item navbar-item-disabled">Map</span>
            <span class="navbar-item navbar-item-disabled">Realtime</span>
            <span class="navbar-item navbar-item-disabled">History</span>
          % end

          <a class="navbar-item" href="{{ get_url(system, 'routes') }}">Routes</a>
          <a class="navbar-item" href="{{ get_url(system, 'blocks') }}">Blocks</a>
          <a class="navbar-item" href="{{ get_url(system, 'about') }}">About</a>
        % end

        % if len(systems) > 1:
          <div class="navbar-item navbar-right dropdown">
            Change System
            <div class="dropdown-content">
              % if system is None:
                <a class="disabled-link">All Systems</a>
              % else:
                <a href="{{ get_url(None, get('path', '')) }}">All Systems</a>
              % end
              % sorted_systems = sorted(systems)
              <table class="dropdown-table">
                <tbody>
                  % for i in range(0, len(sorted_systems), 2):
                    <tr>
                      % left_system = sorted_systems[i]
                      <td>
                        % if system is not None and system == left_system:
                          <a class="disabled-link">{{ left_system }}</a>
                        % else:
                          <a href="{{ get_url(left_system, get('path', '')) }}">{{ left_system }}</a>
                        % end
                      </td>
                      % if i < len(sorted_systems) - 1:
                        % right_system = sorted_systems[i + 1]
                        <td>
                          % if system is not None and system == right_system:
                            <a class="disabled-link">{{ right_system }}</a>
                          % else:
                            <a href="{{ get_url(right_system, get('path', '')) }}">{{ right_system }}</a>
                          % end
                        </td>
                      % end
                    </tr>
                  % end
                </tbody>
              </table>
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
      % if system is None:
        <a class="mobile-navbar-item" href="{{ get_url(None, 'map') }}">Map</a>
        <a class="mobile-navbar-item" href="{{ get_url(None, 'realtime') }}">Realtime</a>
        <a class="mobile-navbar-item" href="{{ get_url(None, 'history') }}">History</a>
        <a class="mobile-navbar-item" href="{{ get_url(None, 'routes') }}">Routes</a>
        <a class="mobile-navbar-item" href="{{ get_url(None, 'blocks') }}">Blocks</a>
        <a class="mobile-navbar-item" href="{{ get_url(None, 'about') }}">About</a>
        
        % if len(systems) > 1:
          % path = get('path', '')
          <a class="mobile-navbar-item" href="{{ get_url(None, f'systems?path={path}') }}">Change System</a>
        % end
      % else:
        % if system.supports_realtime:
          <a class="mobile-navbar-item" href="{{ get_url(system, 'map') }}">Map</a>
          <a class="mobile-navbar-item" href="{{ get_url(system, 'realtime') }}">Realtime</a>
          <a class="mobile-navbar-item" href="{{ get_url(system, 'history') }}">History</a>
        % end

        <a class="mobile-navbar-item" href="{{ get_url(system, 'routes') }}">Routes</a>
        <a class="mobile-navbar-item" href="{{ get_url(system, 'blocks') }}">Blocks</a>
        <a class="mobile-navbar-item" href="{{ get_url(system, 'about') }}">About</a>
        
        % if len(systems) > 1:
          % path = get('path', '')
          <a class="mobile-navbar-item" href="{{ get_url(system, f'systems?path={path}') }}">Change System</a>
        % end
      % end
    </div>

    <div id="sub-navbar">
      <div class="sub-navbar-system">
        % if system is None:
          All Transit Systems
        % else:
          {{ system }} Regional Transit System
        % end
      </div>
      % if system is None or system.supports_realtime:
        <div class="sub-navbar-date">
          Updated {{ last_updated }}
        </div>
      % end
    </div>
    
    <div id="content">
      {{ !base }}
    </div>
  </body>
</html>