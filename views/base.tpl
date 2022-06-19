<html>
    <head> 
        <title>
            % if system is None:
                BCTracker | {{ title }}
            % else:
                {{ system }} | {{ title }}
            % end
        </title>
        
        <link rel="icon" type="image/png" href="/img/favicon-16.png" sizes="16x16" />
        <link rel="icon" type="image/png" href="/img/favicon-32.png" sizes="32x32" />
        <link rel="icon" type="image/png" href="/img/favicon-48.png" sizes="48x48" />
        
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        
        % if system is None:
            <meta property="og:title" content="BCTracker | {{ title }}">
            <meta property="og:description" content="Transit schedules and bus tracking for BC, Canada" />
        % else:
            <meta property="og:title" content="{{ system }} | {{ title }}">
            <meta property="og:description" content="Transit schedules and bus tracking for {{ system }}, BC" />
        % end
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{{ get_url(system) }}" />
        <meta property="og:image" content="{{ get_url(system, 'img/meta-logo.png') }}" />
        <meta property="og:image:type" content="image/png" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:image:alt" content="BCTracker Logo" />
        <meta property="og:site_name" content="BCTracker" />
        
        <link rel="stylesheet" href="/style/main.css?version={{ version }}" />
        
        <link rel="stylesheet" media="screen and (min-width: 1001px)" href="/style/devices/desktop.css?version={{ version }}" />
        <link rel="stylesheet" media="screen and (min-width: 501px) and (max-width: 1000px)" href="/style/devices/tablet.css?version={{ version }}" />
        <link rel="stylesheet" media="screen and (max-width: 500px)" href="/style/devices/mobile.css?version={{ version }}" />
        
        <script>
            let prefersDarkScheme
        </script>
        % if theme == "light":
            <link rel="stylesheet" href="/style/themes/light.css?version={{ version }}" />
            
            <script>
                prefersDarkScheme = false
            </script>
        % elif theme == "dark":
            <link rel="stylesheet" href="/style/themes/dark.css?version={{ version }}" />
            
            <script>
                prefersDarkScheme = true
            </script>
        % elif theme == "classic":
            <link rel="stylesheet" href="/style/themes/classic.css?version={{ version }}" />
            
            <script>
                prefersDarkScheme = false
            </script>
        % elif theme == "bchydro":
            <link rel="stylesheet" href="/style/themes/bchydro.css?version={{ version }}" />
            
            <script>
                prefersDarkScheme = false
            </script>
        % elif theme == "uta":
            <link rel="stylesheet" href="/style/themes/uta.css?version={{ version }}" />
            
            <script>
                prefersDarkScheme = false
            </script>
        % else:
            <link rel="stylesheet" media="screen and (prefers-color-scheme: light)" href="/style/themes/light.css?version={{ version }}" />
            <link rel="stylesheet" media="screen and (prefers-color-scheme: dark)" href="/style/themes/dark.css?version={{ version }}" />
            
            <script>
                prefersDarkScheme = window.matchMedia("screen and (prefers-color-scheme: dark)").matches;
            </script>
        % end
        
        % if defined("include_maps") and include_maps:
            <script src='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.js'></script>
            <link href='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.css' rel='stylesheet' />
            
            <script>
                mapboxgl.accessToken = '{{mapbox_api_key}}';
            </script>
        % end
        
        % if (system is None or system.realtime_enabled) and get('show_refresh_button', False):
            <script>
                const date = new Date();
                const timeToNextUpdate = 60 - date.getSeconds();
                
                setTimeout(function() {
                    const element = document.getElementById("refresh-button")
                    element.classList.remove("hidden");
                    element.onclick = refresh
                }, 1000 * (timeToNextUpdate + 15));
                
                function refresh() {
                    location.reload();
                }
            </script>
        % end
        
        <script>
            function toggleNavigationMenu() {
                document.getElementById("navigation-menu").classList.toggle("display-none");
                document.getElementById("search-non-desktop").classList.add("display-none");
                document.getElementById("change-system-menu").classList.add("display-none");
            }
            
            function toggleChangeSystemMenu() {
                document.getElementById("navigation-menu").classList.add("display-none");
                document.getElementById("search-non-desktop").classList.add("display-none");
                document.getElementById("change-system-menu").classList.toggle("display-none");
            }
            
            String.prototype.format = function() {
                a = this;
                for (k in arguments) {
                    a = a.replace("{" + k + "}", arguments[k])
                }
                return a
            }
            
            function getUrl(systemID, path) {
                if (systemID === null || systemID === undefined) {
                    return "{{ no_system_domain }}".format(path)
                }
                return "{{ system_domain_path if system is None else system_domain }}".format(systemID, path)
            }
            
            function openSurvey() {
                window.open("https://docs.google.com/forms/d/e/1FAIpQLSfxtrvodzaJzmNwt6CQxfDfQcR2F9D6crOrxwCtP6LA6aeCgQ/viewform?usp=sf_link", "_blank").focus();
            }
        </script>
    </head>
    
    <body>
        <div id="header">
            <div id="navigation-bar">
                <a class="navigation-button title" href="{{ get_url(system) }}">BCTracker</a>
                
                <div class="desktop-only">
                    % if system is None or system.realtime_enabled:
                        <a class="navigation-button" href="{{ get_url(system, 'map') }}">Map</a>
                        <a class="navigation-button" href="{{ get_url(system, 'realtime') }}">Realtime</a>
                        <a class="navigation-button" href="{{ get_url(system, 'history') }}">History</a>
                    % else:
                        <span class="navigation-button disabled">Map</span>
                        <span class="navigation-button disabled">Realtime</span>
                        <span class="navigation-button disabled">History</span>
                    % end
                    
                    <a class="navigation-button" href="{{ get_url(system, 'routes') }}">Routes</a>
                    <a class="navigation-button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
                    <a class="navigation-button" href="{{ get_url(system, 'about') }}">About</a>
                    
                    % if len(systems) > 1:
                        <div id="system-dropdown" class="navigation-button dropdown right">
                            Change System
                            <div class="content">
                                % if system is None:
                                    <span class="dropdown-button full-width disabled">All Systems</span>
                                % else:
                                    <a class="dropdown-button full-width" href="{{ get_url(None, path) }}">All Systems</a>
                                % end
                                % realtime_enabled_systems = sorted([s for s in systems if s.realtime_enabled])
                                % realtime_disabled_systems = sorted([s for s in systems if not s.realtime_enabled])
                                % if len(realtime_enabled_systems) > 0:
                                    % if len(realtime_disabled_systems) > 0:
                                        <div class="header">Schedule and Bus Tracking</div>
                                    % end
                                    % for alt_system in realtime_enabled_systems:
                                        % if system is not None and system == alt_system:
                                            <span class="dropdown-button disabled">{{ alt_system }}</span>
                                        % else:
                                            <a class="dropdown-button" href="{{ get_url(alt_system, path) }}">{{ alt_system }}</a>
                                        % end
                                    % end
                                % end
                                % if len(realtime_disabled_systems) > 0:
                                    % if len(realtime_enabled_systems) > 0:
                                        <div class="header">Schedule Only</div>
                                    % end
                                    % for alt_system in realtime_disabled_systems:
                                        % if system is not None and system == alt_system:
                                            <span class="dropdown-button disabled">{{ alt_system }}</span>
                                        % else:
                                            <a class="dropdown-button" href="{{ get_url(alt_system, path) }}">{{ alt_system }}</a>
                                        % end
                                    % end
                                % end
                            </div>
                        </div>
                    % end
                    
                    <div id="search-desktop" class="right">
                        <img src="/img/white/search.png" />
                        <input type="text" id="search-desktop-input" placeholder="Search" oninput="searchDesktop()" onfocus="searchDesktopFocus()" onblur="searchDesktopBlur()">
                        
                        <div id="search-desktop-results" class="display-none"></div>
                    </div>
                </div>
                
                <div class="tablet-only">
                    % if system is None or system.realtime_enabled:
                        <a class="navigation-button" href="{{ get_url(system, 'map') }}">Map</a>
                        <a class="navigation-button" href="{{ get_url(system, 'realtime') }}">Realtime</a>
                    % else:
                        <a class="navigation-button" href="{{ get_url(system, 'routes') }}">Routes</a>
                        <a class="navigation-button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
                    % end
                </div>
                
                <div class="navigation-menu-toggle non-desktop right" onclick="toggleNavigationMenu()">
                    <div class="line"></div>
                    <div class="line"></div>
                    <div class="line"></div>
                </div>
                
                % if len(systems) > 1:
                    <div class="menu-toggle non-desktop right" onclick="toggleChangeSystemMenu()">
                        <img src="/img/white/system.png" />
                    </div>
                % end
                
                <div class="menu-toggle non-desktop right" onclick="toggleSearchNonDesktop()">
                    <img src="/img/white/search.png" />
                </div>
                
                <br style="clear: both" />
            </div>
        
            <div id="navigation-menu" class="menu non-desktop display-none">
                % if system is None or system.realtime_enabled:
                    <a class="menu-button mobile-only" href="{{ get_url(system, 'map') }}">
                        <img src="/img/white/map.png" />
                        <span>Map</span>
                    </a>
                    <a class="menu-button mobile-only" href="{{ get_url(system, 'realtime') }}">
                        <img src="/img/white/realtime.png" />
                        <span>Realtime</span>
                    </a>
                    <a class="menu-button" href="{{ get_url(system, 'history') }}">
                        <img src="/img/white/history.png" />
                        <span>History</span>
                    </a>
                    <a class="menu-button" href="{{ get_url(system, 'routes') }}">
                        <img src="/img/white/routes.png" />
                        <span>Routes</span>
                    </a>
                    <a class="menu-button" href="{{ get_url(system, 'blocks') }}">
                        <img src="/img/white/blocks.png" />
                        <span>Blocks</span>
                    </a>
                % else:
                    <a class="menu-button mobile-only" href="{{ get_url(system, 'routes') }}">
                        <img src="/img/white/routes.png" />
                        <span>Routes</span>
                    </a>
                    <a class="menu-button mobile-only" href="{{ get_url(system, 'blocks') }}">
                        <img src="/img/white/blocks.png" />
                        <span>Blocks</span>
                    </a>
                % end
                
                <a class="menu-button" href="{{ get_url(system, 'about') }}">
                    <img src="/img/white/about.png" />
                    <span>About</span>
                </a>
            </div>
            
            <div id="search-non-desktop" class="menu non-desktop display-none">
                <input type="text" id="search-non-desktop-input" placeholder="Search" oninput="searchNonDesktop()">
                
                <div id="search-non-desktop-results" class="display-none"></div>
            </div>
            
            % if len(systems) > 1:
                <div id="change-system-menu" class="menu non-desktop display-none">
                    % if system is None:
                        <span class="menu-button full-width disabled">All Systems</span>
                    % else:
                        <a class="menu-button full-width" href="{{ get_url(None, path) }}">All Systems</a>
                    % end
                    % realtime_enabled_systems = sorted([s for s in systems if s.realtime_enabled])
                    % realtime_disabled_systems = sorted([s for s in systems if not s.realtime_enabled])
                    % if len(realtime_enabled_systems) > 0:
                        % if len(realtime_disabled_systems) > 0:
                            <div class="header">Schedule and Bus Tracking</div>
                        % end
                        % for alt_system in sorted([s for s in systems if s.realtime_enabled]):
                            % if system is not None and system == alt_system:
                                <span class="menu-button disabled">{{ alt_system }}</span>
                            % else:
                                <a class="menu-button" href="{{ get_url(alt_system, path) }}">{{ alt_system }}</a>
                            % end
                        % end
                    % end
                    % if len(realtime_disabled_systems) > 0:
                        % if len(realtime_enabled_systems) > 0:
                            <div class="header">Schedule Only</div>
                        % end
                        % for alt_system in sorted([s for s in systems if not s.realtime_enabled]):
                            % if system is not None and system == alt_system:
                                <span class="menu-button disabled">{{ alt_system }}</span>
                            % else:
                                <a class="menu-button" href="{{ get_url(alt_system, path) }}">{{ alt_system }}</a>
                            % end
                        % end
                    % end
                </div>
            % end
            
            <div id="system-bar">
                <div class="content">
                    <div id="system">
                        % if system is None:
                            All Transit Systems
                        % else:
                            {{ system }} Regional Transit System
                        % end
                    </div>
                    % if system is None or system.realtime_enabled:
                        <div id="last-updated">Updated {{ last_updated }}</div>
                    % end
                </div>
                % if (system is None or system.realtime_enabled) and get('show_refresh_button', False):
                    <div id="refresh-button" class="hidden">
                        <img src="/img/white/refresh.png" />
                    </div>
                % end
            </div>
            
            % from datetime import datetime
            % if system is not None and (system.id == 'squamish' or system.id == 'whistler') and datetime.now() < datetime(2022, 6, 22):
                <div id="banner">
                    <div class="content">
                        <span class="title">Service in {{ system }} will resume on June 22nd</span>
                        <br />
                        <span class="description">For more information and updates please visit the <a href="https://www.bctransit.com/{{ system.id }}/news">BC Transit News Page</a>.</span>
                    </div>
                </div>
            % end
        </div>
        
        <div id="content">{{ !base }}</div>
    </body>
</html>

<script>
    let selectedResultIndex = 0;
    let searchResults = [];
    let loadingResults = false;
    let enterPending = false;
    
    function searchDesktopFocus() {
        const query = document.getElementById("search-desktop-input").value;
        const element = document.getElementById("search-desktop-results");
        if (query === undefined || query === null || query === "") {
            element.classList.add("display-none");
        } else {
            element.classList.remove("display-none");
        }
    }
    
    function searchDesktopBlur() {
        setTimeout(function() {
            const element = document.getElementById("search-desktop-results");
            element.classList.add("display-none");
        }, 200);
    }
    
    function searchDesktop() {
        const inputElement = document.getElementById("search-desktop-input");
        const resultsElement = document.getElementById("search-desktop-results");
        search(inputElement, resultsElement, false);
    }
    
    function toggleSearchNonDesktop() {
        const element = document.getElementById("search-non-desktop");
        element.classList.toggle("display-none");
        if (!element.classList.contains("display-none")) {
            document.getElementById("search-non-desktop-input").focus();
        }
        document.getElementById("navigation-menu").classList.add("display-none");
        document.getElementById("change-system-menu").classList.add("display-none");
    }
    
    function searchNonDesktop() {
        const inputElement = document.getElementById("search-non-desktop-input");
        const resultsElement = document.getElementById("search-non-desktop-results");
        search(inputElement, resultsElement, true);
    }
    
    function setSelectedEntry(newIndex) {
        const oldElement = searchResults[selectedResultIndex].element;
        oldElement.classList.remove("keyboard-selected");
        
        const newElement = searchResults[newIndex].element;
        newElement.classList.add("keyboard-selected");
        
        selectedResultIndex = newIndex;
    }
    
    function clearSearchHighlighting() { 
        if (searchResults && searchResults.length > 0 && searchResults[selectedResultIndex]) {
            const element = searchResults[selectedResultIndex].element;
            element.classList.remove("keyboard-selected"); 
        }
        selectedResultIndex = 0;
        searchResults = [];
    }
    
    function handleResultsDown() {
        if (searchResults.length < 2){
            return; // Nothing to change for 0 or 1 results
        }
        if (selectedResultIndex === searchResults.length - 1){
            return; // Can't go down from the last result
        }
      
        setSelectedEntry(selectedResultIndex + 1);
    }

    function handleResultsUp() {
        if (searchResults.length < 2){
            return; // Nothing to change for 0 or 1 results
        }
        if (selectedResultIndex === 0){
            return; // Can't go up from the first result
        }
      
        setSelectedEntry(selectedResultIndex - 1);
    }
    
    function handleResultsEnter() {
        if (loadingResults) {
            enterPending = true;
        } else if (searchResults && searchResults.length > 0 && searchResults[selectedResultIndex]) {
            window.location = searchResults[selectedResultIndex].url;
        }
    }

    function search(inputElement, resultsElement, useLightIcons) {
        const query = inputElement.value;
        if (query === undefined || query === null || query === "") {
            resultsElement.classList.add("display-none");
            resultsElement.innerHTML = "";
            inputElement.onkeyup = function() {};
        } else {
            loadingResults = true;
            resultsElement.classList.remove("display-none");
            if (resultsElement.innerHTML === "") {
                resultsElement.innerHTML = "<div class='message'>Loading...</div>";
            }
            const request = new XMLHttpRequest();
            request.open("POST", "{{get_url(system, 'api/search')}}", true);
            request.responseType = "json";
            request.onload = function() {
                const count = request.response.count;
                if (count === 0) {
                    resultsElement.innerHTML = "<div class='message'>No Results</div>";
                    inputElement.onkeyup = function() {};
                } else {
                    const results = request.response.results;
                    resultsElement.innerHTML = getSearchHTML(results, count, useLightIcons);
                    
                    // Reset navigation
                    clearSearchHighlighting();
                    
                    // Save the global array of results, including their URL and the HTML element reference for them
                    searchResults = results.map(function(result, index) {
                      return { 
                        url: result.url, 
                        element: document.getElementById("search-result-entry-" + index)
                      }
                    });
                    
                    setSelectedEntry(0);
                    inputElement.onkeyup = function(event) {
                        if (event.keyCode === 13) { // ENTER
                            event.preventDefault();
                            handleResultsEnter();
                            return;
                        }
                        if (event.keyCode === 38) { // ARROW KEY UP
                            event.preventDefault();
                            handleResultsUp();
                            return;
                        }
                        if (event.keyCode === 40) { // ARROW KEY DOWN
                            event.preventDefault();
                            handleResultsDown();
                        }
                    };
                    inputElement.onkeydown = function(event) {
                        // Prevent up/down presses from moving cursor
                        if (event.keyCode === 38 || event.keyCode === 40) {
                            event.preventDefault();
                            event.stopPropagation();
                        }
                    };
                }
                loadingResults = false;
                if (enterPending) {
                    enterPending = false;
                    handleResultsEnter();
                }
            };
            request.onerror = function() {
                resultsElement.innerHTML = "<div class='message'>Error loading search results</div>";
                inputElement.onkeyup = function() {};
                loadingResults = false;
            };
            const data = new FormData()
            data.set("query", query)
            request.send(data);
        }
    }
    
    function getSearchHTML(results, count, useLightIcons) {
        let html = "";
        if (count === 1) {
            html += "<div class='message smaller-font'>Showing 1 of 1 result</div>";
        } else {
            html += "<div class='message smaller-font'>Showing " + results.length + " of " + count + " results</div>";
        }
        for (i = 0; i < results.length; i++) {
            const result = results[i]
            let icon = "";
            let name = result.name;
            switch (result.type) {
                case "bus":
                    if (prefersDarkScheme || useLightIcons) {
                        icon = "<img src='/img/white/realtime.png' />";
                    } else {
                        icon = "<img src='/img/black/realtime.png' />";
                    }
                    name = "Bus " + result.name;
                    break;
                case "route":
                    if (prefersDarkScheme || useLightIcons) {
                        icon = "<img src='/img/white/routes.png' />";
                    } else {
                        icon = "<img src='/img/black/routes.png' />";
                    }
                    name = "Route " + result.name;
                    break;
                case "stop":
                    if (prefersDarkScheme || useLightIcons) {
                        icon = "<img src='/img/white/stop.png' />";
                    } else {
                        icon = "<img src='/img/black/stop.png' />";
                    }
                    name = "Stop " + result.name;
                    break;
                default:
                    break;
            }
            html += "\
                <a id='search-result-entry-" + i + "' href='" + result.url + "'>" +
                    icon +
                    "<div class='description'>" +
                        name +
                        "<br />\
                        <span class='smaller-font lighter-text'>" + result.description + "</span>\
                    </div>\
                </a>";
        }
        return html;
    }
</script>
