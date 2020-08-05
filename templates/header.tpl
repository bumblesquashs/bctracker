<html>
  <head> 
    <title>{{title}}</title>
    
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
        <a class="navbar-item" href="/realtime">Realtime</a>
        <a class="navbar-item" href="/routes">All Routes</a>
        <a class="navbar-item" href="/blocks">All Blocks</a>
        <a class="navbar-item" href="/history">Vehicle History</a>
        <a class="navbar-item" href="/about">About</a>
      </div>

      <div class="mobile-navbar-toggle mobile-only" onclick="toggleMobileNavbar()">
        <div class="mobile-navbar-toggle-line"></div>
        <div class="mobile-navbar-toggle-line"></div>
        <div class="mobile-navbar-toggle-line"></div>
      </div>
    </div>
    
    <div id="mobile-navbar" class="mobile-only display-none">
      <a class="mobile-navbar-item" href="/realtime">Realtime</a>
      <a class="mobile-navbar-item" href="/routes">All Routes</a>
      <a class="mobile-navbar-item" href="/blocks">All Blocks</a>
      <a class="mobile-navbar-item" href="/history">Vehicle History</a>
      <a class="mobile-navbar-item" href="/about">About</a>
    </div>
    
    <div id="content">
