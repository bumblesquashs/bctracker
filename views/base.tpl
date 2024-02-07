<html>
    <head>
        % if config.enable_analytics:
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id={{ config.analytics_key }}"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag("js", new Date());
                gtag("config", "{{ config.analytics_key }}");
            </script>
        % end
        
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
        
        % if get('disable_indexing', False):
            <meta name="robots" content="noindex">
        % end
        
        % if system is None:
            <meta property="og:title" content="BCTracker | {{ title }}">
            <meta property="og:description" content="Transit schedules and bus tracking for BC, Canada" />
        % else:
            <meta property="og:title" content="{{ system }} | {{ title }}">
            <meta property="og:description" content="Transit schedules and bus tracking for {{ system }}, BC" />
        % end
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{{ get_url(system, path) }}" />
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
        
        % if theme is None:
            <link rel="stylesheet" media="screen and (prefers-color-scheme: light)" href="/style/themes/light.css?version={{ version }}" />
            <link rel="stylesheet" media="screen and (prefers-color-scheme: dark)" href="/style/themes/dark.css?version={{ version }}" />
        % else:
            <link rel="stylesheet" href="/style/themes/{{ theme.id }}.css?version={{ version }}" />
        % end
        
        % if include_maps:
            <script src="https://cdn.jsdelivr.net/npm/ol@v8.2.0/dist/ol.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v8.2.0/ol.css">
        % end
        
        % if enable_refresh and (system is None or system.realtime_enabled):
            <script>
                const date = new Date();
                const timeToNextUpdate = 60 - date.getSeconds();
                
                setTimeout(function() {
                    const element = document.getElementById("refresh-button")
                    element.classList.remove("disabled");
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
            }
            
            function toggleSystemMenu() {
                document.getElementById("system-menu").classList.toggle("collapse-non-desktop");
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
                    return "{{ config.all_systems_domain }}".format(path)
                }
                return "{{ config.system_domain_path if system is None else config.system_domain }}".format(systemID, path)
            }
            
            function setCookie(key, value) {
                const max_age = 60*60*24*365*10;
                if ("{{ config.cookie_domain }}" == "None") {
                    document.cookie = key + "=" + value + "; max_age=" + max_age + "; path=/";
                } else {
                    document.cookie = key + "=" + value + "; max_age=" + max_age + "; domain={{ config.cookie_domain }}; path=/";
                }
            }
            
            function openSurvey() {
                window.open("https://docs.google.com/forms/d/e/1FAIpQLSegYbUi18Qrm40GSAYIel8NEH3r67vBpJXHGbEqEt2xwDOu9A/viewform?usp=sf_link", "_blank").focus();
                hideSurvey();
            }
            
            function hideSurvey() {
                document.getElementById("survey-banner").classList.add("display-none");
                const now = new Date();
                const expireTime = now.getTime() + 1000 * 60 * 60 * 24 * 60;
                now.setTime(expireTime);
                
                document.cookie = "survey_banner=hide;expires=" + now.toUTCString() + ";domain={{ '' if config.cookie_domain is None else config.cookie_domain }};path=/";
            }
        </script>
    </head>
    
    <body class="{{ 'full-map' if full_map else '' }} {{ 'side-bar-closed' if hide_systems else 'side-bar-open' }}">
        <a id="title" href="{{ get_url(system) }}">
            <img class="white" src="/img/white/bctracker.png" />
            <img class="black" src="/img/black/bctracker.png" />
            <div class="side-bar-open-only">BCTracker</div>
        </a>
        <div id="navigation-bar">
            <a class="navigation-item title non-desktop" href="{{ get_url(system) }}">BCTracker</a>
            
            % if system is None or system.realtime_enabled:
                <a class="navigation-item non-mobile" href="{{ get_url(system, 'map') }}">Map</a>
                <a class="navigation-item non-mobile" href="{{ get_url(system, 'realtime') }}">Realtime</a>
                <a class="navigation-item desktop-only" href="{{ get_url(system, 'history') }}">History</a>
            % else:
                <span class="navigation-item desktop-only disabled">Map</span>
                <span class="navigation-item desktop-only disabled">Realtime</span>
                <span class="navigation-item desktop-only disabled">History</span>
                
                <a class="navigation-item tablet-only" href="{{ get_url(system, 'routes') }}">Routes</a>
                <a class="navigation-item tablet-only" href="{{ get_url(system, 'blocks') }}">Blocks</a>
            % end
            
            <a class="navigation-item desktop-only" href="{{ get_url(system, 'routes') }}">Routes</a>
            <a class="navigation-item desktop-only" href="{{ get_url(system, 'blocks') }}">Blocks</a>
            
            <a class="navigation-item desktop-only" href="{{ get_url(system, 'about') }}">About</a>
            
            <div class="flex-1"></div>
            
            <a class="navigation-icon desktop-only tooltip-anchor" href="{{ get_url(system, 'nearby') }}">
                <img class="white" src="/img/white/location.png" />
                <img class="black" src="/img/black/location.png" />
                <div class="tooltip">
                    <div class="title">Nearby Stops</div>
                </div>
            </a>
            
            <a class="navigation-icon desktop-only tooltip-anchor" href="{{ get_url(system, 'personalize') }}">
                <img class="white" src="/img/white/personalize.png" />
                <img class="black" src="/img/black/personalize.png" />
                <div class="tooltip">
                    <div class="title">Personalize</div>
                </div>
            </a>
            
            <div id="search-desktop" class="desktop-only">
                <img class="white" src="/img/white/search.png" />
                <img class="black" src="/img/black/search.png" />
                <input type="text" id="search-desktop-input" placeholder="Search" oninput="searchDesktop()" onfocus="searchDesktopFocus()" onblur="searchDesktopBlur()">
                
                <div id="search-desktop-results" class="display-none"></div>
            </div>
            
            <div id="search-non-desktop-toggle" onclick="toggleSearchNonDesktop()">
                <img class="white" src="/img/white/search.png" />
                <img class="black" src="/img/black/search.png" />
            </div>
            
            <div id="navigation-menu-toggle" onclick="toggleNavigationMenu()">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
            </div>
        </div>
        <div id="navigation-menu" class="menu non-desktop display-none">
            % if system is None or system.realtime_enabled:
                <a class="menu-button mobile-only" href="{{ get_url(system, 'map') }}">
                    <img class="white" src="/img/white/map.png" />
                    <img class="black" src="/img/black/map.png" />
                    <span>Map</span>
                </a>
                <a class="menu-button mobile-only" href="{{ get_url(system, 'realtime') }}">
                    <img class="white" src="/img/white/realtime.png" />
                    <img class="black" src="/img/black/realtime.png" />
                    <span>Realtime</span>
                </a>
                <a class="menu-button" href="{{ get_url(system, 'history') }}">
                    <img class="white" src="/img/white/history.png" />
                    <img class="black" src="/img/black/history.png" />
                    <span>History</span>
                </a>
                <a class="menu-button" href="{{ get_url(system, 'routes') }}">
                    <img class="white" src="/img/white/route.png" />
                    <img class="black" src="/img/black/route.png" />
                    <span>Routes</span>
                </a>
                <a class="menu-button" href="{{ get_url(system, 'blocks') }}">
                    <img class="white" src="/img/white/block.png" />
                    <img class="black" src="/img/black/block.png" />
                    <span>Blocks</span>
                </a>
            % else:
                <a class="menu-button mobile-only" href="{{ get_url(system, 'routes') }}">
                    <img class="white" src="/img/white/route.png" />
                    <img class="black" src="/img/black/route.png" />
                    <span>Routes</span>
                </a>
                <a class="menu-button mobile-only" href="{{ get_url(system, 'blocks') }}">
                    <img class="white" src="/img/white/block.png" />
                    <img class="black" src="/img/black/block.png" />
                    <span>Blocks</span>
                </a>
            % end
            
            <a class="menu-button" href="{{ get_url(system, 'about') }}">
                <img class="white" src="/img/white/about.png" />
                <img class="black" src="/img/black/about.png" />
                <span>About</span>
            </a>
            <a class="menu-button" href="{{ get_url(system, 'nearby') }}">
                <img class="white" src="/img/white/location.png" />
                <img class="black" src="/img/black/location.png" />
                <span>Nearby</span>
            </a>
            <a class="menu-button" href="{{ get_url(system, 'personalize') }}">
                <img class="white" src="/img/white/personalize.png" />
                <img class="black" src="/img/black/personalize.png" />
                <span>Personalize</span>
            </a>
        </div>
        <div id="search-non-desktop" class="menu non-desktop display-none">
            <input type="text" id="search-non-desktop-input" placeholder="Search" oninput="searchNonDesktop()">
            <div id="search-non-desktop-results" class="display-none"></div>
        </div>
        <div id="side-bar">
            <div id="status" class="side-bar-open-only">
                <div id="system-menu-toggle" onclick="toggleSystemMenu()">
                    <img class="white" src="/img/white/system.png" />
                    <img class="black" src="/img/black/system.png" />
                </div>
                <div class="content">
                    <div id="system">
                        % if system is None:
                            All Transit Systems
                        % else:
                            {{ system }}
                        % end
                    </div>
                    <div id="last-updated">
                        % if system is None or (system.is_loaded and system.realtime_enabled):
                            Updated {{ last_updated }}
                        % end
                    </div>
                </div>
                
                <div id="refresh-button" class="disabled">
                    <img class="white" src="/img/white/refresh.png" />
                    <img class="black" src="/img/black/refresh.png" />
                </div>
            </div>
            <div id="system-menu" class="collapse-non-desktop side-bar-open-only">
                % if system is None:
                    <span class="system-button current all-systems">All Transit Systems</span>
                % else:
                    <a href="{{ get_url(None, path, **path_args) }}" class="system-button all-systems">All Transit Systems</a>
                % end
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if len(region_systems) > 0:
                        <div class="header">{{ region }}</div>
                        % for region_system in region_systems:
                            % if system is not None and system == region_system:
                                <span class="system-button current">{{ region_system }}</span>
                            % else:
                                <a href="{{ get_url(region_system, path, **path_args) }}" class="system-button">{{ region_system }}</a>
                            % end
                        % end
                    % end
                % end
            </div>
            <div class="flex-1 side-bar-closed-only"></div>
            <div id="side-bar-toggle-container">
                <div id="side-bar-toggle" onclick="toggleSideBar()">
                    <div class="side-bar-open-only">&laquo;</div>
                    <div class="side-bar-closed-only">&raquo;</div>
                </div>
                <div class="side-bar-open-only">Hide Systems</div>
            </div>
        </div>
        <div id="main">
            <div id="banners">
                % from models.date import Date
                % if system is not None and (system.id == 'comox' or system.id == 'campbell-river') and Date.today(system.timezone) < Date(2024, 2, 12, system.timezone):
                    <div class="banner">
                        <div class="content">
                            <div class="title">Service in {{ system }} will resume on February 12th</div>
                            % bct_id = 'comox-valley' if system.id == 'comox' else system.id
                            <div class="description">For more information and updates please visit the <a href="https://www.bctransit.com/{{ bct_id }}/news">BC Transit News Page</a>.</div>
                        </div>
                    </div>
                % end
            </div>
            <div id="content">{{ !base }}</div>
        </div>
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
        search(inputElement, resultsElement);
    }
    
    function toggleSearchNonDesktop() {
        const element = document.getElementById("search-non-desktop");
        element.classList.toggle("display-none");
        if (!element.classList.contains("display-none")) {
            document.getElementById("search-non-desktop-input").focus();
        }
        document.getElementById("navigation-menu").classList.add("display-none");
    }
    
    function searchNonDesktop() {
        const inputElement = document.getElementById("search-non-desktop-input");
        const resultsElement = document.getElementById("search-non-desktop-results");
        search(inputElement, resultsElement);
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

    function search(inputElement, resultsElement) {
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
                    resultsElement.innerHTML = getSearchHTML(results, count);
                    
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
    
    function getSearchHTML(results, count) {
        let html = "";
        if (count === 1) {
            html += "<div class='message smaller-font'>Showing 1 of 1 result</div>";
        } else {
            html += "<div class='message smaller-font'>Showing " + results.length + " of " + count + " results</div>";
        }
        for (i = 0; i < results.length; i++) {
            const result = results[i]
            const icon = "<img class='white' src='/img/white/" + result.icon + ".png' /><img class='black' src='/img/black/" + result.icon + ".png' />";
            let name = result.name;
            switch (result.type) {
                case "block":
                    name = "Block " + result.name;
                    break;
                case "bus":
                    name = "Bus " + result.name;
                    break;
                case "route":
                    name = "Route " + result.name;
                    break;
                case "stop":
                    name = "Stop " + result.name;
                    break;
                default:
                    break;
            }
            html += "\
                <a id='search-result-entry-" + i + "' class='result' href='" + result.url + "'>" +
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
    
    function toggleSideBar() {
        const element = document.getElementsByTagName("body")[0];
        element.classList.toggle("side-bar-open");
        element.classList.toggle("side-bar-closed");
        if (element.classList.contains("side-bar-open")) {
            setCookie("hide_systems", "no");
        } else {
            setCookie("hide_systems", "yes");
        }
        if (map !== undefined) {
            map.updateSize();
        }
    }
</script>
