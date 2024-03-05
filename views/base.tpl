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
        <meta property="og:url" content="{{ get_url(system, agency, path) }}" />
        <meta property="og:image" content="{{ get_url(system, agency, '/img/meta-logo.png') }}" />
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
            <script src="/js/area.js"></script>
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
                document.getElementById("search").classList.add("display-none");
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
            
            function getUrl(systemID, agencyID, path) {
                if (systemID !== undefined && systemID !== null) {
                    return "{{ config.system_domain_path if system is None else config.system_domain }}".format(systemID) + path
                }
                if (agencyID !== undefined && agencyID !== null) {
                    return "{{ config.agency_domain_path if system is None else config.agency_domain }}".format(agencyID) + path
                }
                return "{{ config.global_domain }}".format(path)
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
        <a id="title" href="{{ get_url(system, agency) }}">
            <img class="white" src="/img/white/bctracker.png" />
            <img class="black" src="/img/black/bctracker.png" />
            <div class="side-bar-open-only">BCTracker</div>
        </a>
        <div id="navigation-bar">
            <a class="navigation-item title non-desktop" href="{{ get_url(system, agency) }}">BCTracker</a>
            
            % if system is None or system.realtime_enabled:
                <a class="navigation-item non-mobile" href="{{ get_url(system, agency, '/map') }}">Map</a>
                <a class="navigation-item non-mobile" href="{{ get_url(system, agency, '/realtime') }}">Realtime</a>
                <a class="navigation-item desktop-only" href="{{ get_url(system, agency, '/history') }}">History</a>
            % else:
                <span class="navigation-item desktop-only disabled">Map</span>
                <span class="navigation-item desktop-only disabled">Realtime</span>
                <span class="navigation-item desktop-only disabled">History</span>
                
                <a class="navigation-item tablet-only" href="{{ get_url(system, agency, '/routes') }}">Routes</a>
                <a class="navigation-item tablet-only" href="{{ get_url(system, agency, '/blocks') }}">Blocks</a>
            % end
            
            <a class="navigation-item desktop-only" href="{{ get_url(system, agency, '/routes') }}">Routes</a>
            <a class="navigation-item desktop-only" href="{{ get_url(system, agency, '/blocks') }}">Blocks</a>
            
            <a class="navigation-item desktop-only" href="{{ get_url(system, agency, '/about') }}">About</a>
            
            <div class="flex-1"></div>
            
            <a class="navigation-icon desktop-only tooltip-anchor" href="{{ get_url(system, agency, '/nearby') }}">
                <img class="white" src="/img/white/location.png" />
                <img class="black" src="/img/black/location.png" />
                <div class="tooltip left">
                    <div class="title">Nearby Stops</div>
                </div>
            </a>
            
            <a class="navigation-icon desktop-only tooltip-anchor" href="{{ get_url(system, agency, '/personalize') }}">
                <img class="white" src="/img/white/personalize.png" />
                <img class="black" src="/img/black/personalize.png" />
                <div class="tooltip left">
                    <div class="title">Personalize</div>
                </div>
            </a>
            
            <div class="navigation-icon" onclick="toggleSearch()">
                <div>
                    <img class="white" src="/img/white/search.png" />
                    <img class="black" src="/img/black/search.png" />
                </div>
                <div class="label">Search</div>
            </div>
            
            <div id="navigation-menu-toggle" onclick="toggleNavigationMenu()">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
            </div>
        </div>
        <div id="navigation-menu" class="non-desktop display-none">
            % if system is None or system.realtime_enabled:
                <a class="menu-button mobile-only" href="{{ get_url(system, agency, '/map') }}">
                    <img class="white" src="/img/white/map.png" />
                    <img class="black" src="/img/black/map.png" />
                    <span>Map</span>
                </a>
                <a class="menu-button mobile-only" href="{{ get_url(system, agency, '/realtime') }}">
                    <img class="white" src="/img/white/realtime.png" />
                    <img class="black" src="/img/black/realtime.png" />
                    <span>Realtime</span>
                </a>
                <a class="menu-button" href="{{ get_url(system, agency, '/history') }}">
                    <img class="white" src="/img/white/history.png" />
                    <img class="black" src="/img/black/history.png" />
                    <span>History</span>
                </a>
                <a class="menu-button" href="{{ get_url(system, agency, '/routes') }}">
                    <img class="white" src="/img/white/route.png" />
                    <img class="black" src="/img/black/route.png" />
                    <span>Routes</span>
                </a>
                <a class="menu-button" href="{{ get_url(system, agency, '/blocks') }}">
                    <img class="white" src="/img/white/block.png" />
                    <img class="black" src="/img/black/block.png" />
                    <span>Blocks</span>
                </a>
            % else:
                <a class="menu-button mobile-only" href="{{ get_url(system, agency, '/routes') }}">
                    <img class="white" src="/img/white/route.png" />
                    <img class="black" src="/img/black/route.png" />
                    <span>Routes</span>
                </a>
                <a class="menu-button mobile-only" href="{{ get_url(system, agency, '/blocks') }}">
                    <img class="white" src="/img/white/block.png" />
                    <img class="black" src="/img/black/block.png" />
                    <span>Blocks</span>
                </a>
            % end
            
            <a class="menu-button" href="{{ get_url(system, agency, '/about') }}">
                <img class="white" src="/img/white/about.png" />
                <img class="black" src="/img/black/about.png" />
                <span>About</span>
            </a>
            <a class="menu-button" href="{{ get_url(system, agency, '/nearby') }}">
                <img class="white" src="/img/white/location.png" />
                <img class="black" src="/img/black/location.png" />
                <span>Nearby</span>
            </a>
            <a class="menu-button" href="{{ get_url(system, agency, '/personalize') }}">
                <img class="white" src="/img/white/personalize.png" />
                <img class="black" src="/img/black/personalize.png" />
                <span>Personalize</span>
            </a>
        </div>
        <div id="side-bar">
            <div id="status" class="side-bar-open-only">
                <div id="system-menu-toggle" onclick="toggleSystemMenu()">
                    <img class="white" src="/img/white/system.png" />
                    <img class="black" src="/img/black/system.png" />
                </div>
                <div class="details">
                    <div id="system">
                        % if system:
                            {{ system }}
                        % elif agency:
                            {{ agency }}
                        % else:
                            All Transit Agencies
                        % end
                    </div>
                    % if last_updated:
                        <div id="last-updated">
                            Updated {{ last_updated }}
                        </div>
                    % end
                </div>
                <div id="refresh-button" class="disabled">
                    <img class="white" src="/img/white/refresh.png" />
                    <img class="black" src="/img/black/refresh.png" />
                </div>
            </div>
            <div id="system-menu" class="collapse-non-desktop side-bar-open-only">
                % if system or agency:
                    <a href="{{ get_url(None, None, path, **path_args) }}" class="system-button all-systems">All Transit Agencies</a>
                % else:
                    <span class="system-button current all-systems">All Transit Agencies</span>
                % end
                % for list_agency in agencies:
                    % if agency and agency == list_agency:
                        <span class="system-button current">{{ list_agency }}</span>
                    % else:
                        <a href="{{ get_url(system, list_agency, path, **path_args) }}" class="system-button">{{ list_agency }}</a>
                    % end
                % end
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if len(region_systems) > 0:
                        <div class="header">{{ region }}</div>
                        % for region_system in sorted(region_systems):
                            % if system and system == region_system:
                                <span class="system-button current">{{ region_system }}</span>
                            % else:
                                <a href="{{ get_url(region_system, agency, path, **path_args) }}" class="system-button">{{ region_system }}</a>
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
                
            </div>
            <div id="page">{{ !base }}</div>
        </div>
        <div id="search" class="display-none" tabindex="0">
            <div id="search-header">
                <div id="search-bar">
                    <input type="text" id="search-input" placeholder="Search" oninput="searchInputChanged()">
                </div>
                % if system is not None:
                    <div id="search-filters">
                        <div class="flex-1">Filters:</div>
                        <div id="search-filter-bus" class="button tooltip-anchor" onclick="toggleSearchBusFilter()">
                            <img class="white" src="/img/white/bus.png" />
                            <img class="black" src="/img/black/bus.png" />
                            <div class="tooltip left">Include Buses</div>
                        </div>
                        <div id="search-filter-route" class="button tooltip-anchor" onclick="toggleSearchRouteFilter()">
                            <img class="white" src="/img/white/route.png" />
                            <img class="black" src="/img/black/route.png" />
                            <div class="tooltip left">Include Routes</div>
                        </div>
                        <div id="search-filter-stop" class="button tooltip-anchor" onclick="toggleSearchStopFilter()">
                            <img class="white" src="/img/white/stop.png" />
                            <img class="black" src="/img/black/stop.png" />
                            <div class="tooltip left">Include Stops</div>
                        </div>
                        <div id="search-filter-block" class="button tooltip-anchor" onclick="toggleSearchBlockFilter()">
                            <img class="white" src="/img/white/block.png" />
                            <img class="black" src="/img/black/block.png" />
                            <div class="tooltip left">Include Blocks</div>
                        </div>
                    </div>
                % end
            </div>
            <div id="search-placeholder">
                % if system is None:
                    Search for buses in all systems
                % else:
                    Search for buses, routes, stops, and blocks in {{ system }}
                % end
            </div>
            <div id="search-results" class="display-none">
                
            </div>
            <div id="search-paging" class="display-none">
                <div id="search-paging-previous" class="button" onclick="searchPreviousPage()">&lt;</div>
                <div id="search-count" class="flex-1">
                    
                </div>
                <div id="search-paging-next" class="button" onclick="searchNextPage()">&gt;</div>
            </div>
        </div>
    </body>
</html>

<script>
    const resultsPerPage = 10;
    
    let showSearch = false;
    
    let selectedResultIndex = 0;
    let searchResults = [];
    let searchPage = 0;
    let loadingResults = false;
    let enterPending = false;
    
    let searchIncludeBuses = true;
    let searchIncludeRoutes = true;
    let searchIncludeStops = true;
    let searchIncludeBlocks = true;
    
    function toggleSearch() {
        const searchElement = document.getElementById("search");
        const inputElement = document.getElementById("search-input");
        const menuElement = document.getElementById("navigation-menu");
        
        showSearch = !showSearch;
        if (showSearch) {
            searchElement.classList.remove("display-none");
            menuElement.classList.add("display-none");
            inputElement.focus();
        } else {
            searchElement.classList.add("display-none");
        }
        if ("map" in window) {
            map.resize();
        }
    }
    
    function search() {
        const inputElement = document.getElementById("search-input");
        const placeholderElement = document.getElementById("search-placeholder");
        const query = inputElement.value;
        
        if (query === undefined || query === null || query === "") {
            updateSearchView([], 0, "{{ 'Search for buses in all systems' if system is None else f'Search for buses, routes, stops, and blocks in {system}' }}");
        } else {
            loadingResults = true;
            if (searchResults.length === 0) {
                placeholderElement.innerHTML = "Loading...";
            }
            const request = new XMLHttpRequest();
            request.open("POST", "{{ get_url(system, agency, '/api/search') }}", true);
            request.responseType = "json";
            request.onload = function() {
                const results = request.response.results;
                const total = request.response.total;
                
                updateSearchView(results, total, total === 0 ? "No Results" : "Results");
                
                if (enterPending) {
                    enterPending = false;
                    handleResultsEnter();
                }
            };
            request.onerror = function() {
                updateSearchView([], 0, "Error loading search results");
            };
            const data = new FormData();
            data.set("query", query);
            data.set("page", searchPage);
            data.set("count", resultsPerPage);
            data.set("include_buses", searchIncludeBuses ? 1 : 0);
            data.set("include_routes", searchIncludeRoutes ? 1 : 0);
            data.set("include_stops", searchIncludeStops ? 1 : 0);
            data.set("include_blocks", searchIncludeBlocks ? 1 : 0);
            request.send(data);
        }
    }
    
    function buildSearchResultElement(index, result) {
        const element = document.createElement("a");
        element.id = "search-result-entry-" + index;
        element.classList.add("result");
        element.href = result.url;
        
        const lightIcon = document.createElement("img");
        lightIcon.classList.add("white");
        lightIcon.src = "/img/white/" + result.icon + ".png";
        element.appendChild(lightIcon);
        
        const darkIcon = document.createElement("img");
        darkIcon.classList.add("black");
        darkIcon.src = "/img/black/" + result.icon + ".png";
        element.appendChild(darkIcon);
        
        const details = document.createElement("div");
        details.classList.add("details");
        
        const name = document.createElement("div");
        name.classList.add("name")
        name.innerHTML = result.name;
        details.appendChild(name);
        
        const description = document.createElement("div");
        description.classList.add("description");
        description.innerHTML = result.description;
        details.appendChild(description);
        
        element.appendChild(details);
        
        return element;
    }
    
    function updateSearchView(results, total, message) {
        const placeholderElement = document.getElementById("search-placeholder");
        const pagingElement = document.getElementById("search-paging");
        const countElement = document.getElementById("search-count");
        const resultsElement = document.getElementById("search-results");
        
        loadingResults = false;
        selectedResultIndex = 0;
        
        if (total === 0) {
            placeholderElement.classList.remove("display-none");
            placeholderElement.innerHTML = message;
            pagingElement.classList.add("display-none");
            countElement.innerHTML = "";
            resultsElement.classList.add("display-none");
            resultsElement.innerHTML = "";
            
            searchResults = [];
        } else {
            placeholderElement.classList.add("display-none");
            placeholderElement.innerHTML = "";
            pagingElement.classList.remove("display-none");
            const min = (searchPage * resultsPerPage) + 1;
            const max = Math.min(total, min + resultsPerPage - 1);
            if (total === 1) {
                countElement.innerHTML = "Showing 1 of 1 result";
            } else {
                countElement.innerHTML = "Showing " + min + " to " + max + " of " + total + " results";
            }
            resultsElement.classList.remove("display-none");
            resultsElement.innerHTML = "";
            for (i = 0; i < results.length; i++) {
                resultsElement.appendChild(buildSearchResultElement(i, results[i]))
            }
            
            searchResults = results.map(function(result, index) {
                return {
                    url: result.url,
                    element: document.getElementById("search-result-entry-" + index)
                }
            });
            setSelectedEntry(0);
        }
        
        updatePagingButtons(total);
        updateKeyboardPressHandlers(total);
    }
    
    function updatePagingButtons(total) {
        const previousButton = document.getElementById("search-paging-previous");
        const nextButton = document.getElementById("search-paging-next");
        if (searchPage === 0) {
            previousButton.classList.add("disabled");
            previousButton.onclick = function() {};
        } else {
            previousButton.classList.remove("disabled");
            previousButton.onclick = searchPreviousPage;
        }
        if ((searchPage * resultsPerPage) >= (total - resultsPerPage)) {
            nextButton.classList.add("disabled");
            nextButton.onclick = function() {};
        } else {
            nextButton.classList.remove("disabled");
            nextButton.onclick = searchNextPage;
        }
    }
    
    function updateKeyboardPressHandlers(total) {
        const searchElement = document.getElementById("search");
        if (total == 0) {
            searchElement.onkeyup = function() {};
            searchElement.onkeydown = function() {};
        } else {
            searchElement.onkeyup = function(event) {
                if (event.keyCode === 13) { // ENTER
                    event.preventDefault();
                    searchResultsEnter();
                }
                if (event.keyCode === 37) { // ARROW KEY LEFT
                    event.preventDefault();
                    searchPreviousPage();
                }
                if (event.keyCode === 38) { // ARROW KEY UP
                    event.preventDefault();
                    searchResultsUp();
                }
                if (event.keyCode === 39) { // ARROW KEY RIGHT
                    event.preventDefault();
                    if ((searchPage + 1) * resultsPerPage < total) {
                        searchNextPage();
                    }
                }
                if (event.keyCode === 40) { // ARROW KEY DOWN
                    event.preventDefault();
                    searchResultsDown();
                }
            };
            searchElement.onkeydown = function(event) {
                // Prevent up/down presses from moving cursor
                if ([37, 38, 39, 40].includes(event.keyCode)) {
                    event.preventDefault();
                    event.stopPropagation();
                }
            };
        }
    }
    
    function searchResultsEnter() {
        if (loadingResults) {
            enterPending = true;
        } else if (selectedResultIndex !== null) {
            window.location = searchResults[selectedResultIndex].url;
        }
    }
    
    function searchResultsDown() {
        if (searchResults.length < 2) {
            return; // Nothing to change for 0 or 1 results
        }
        if (selectedResultIndex === searchResults.length - 1) {
            return; // Can't go down from the last result
        }
        setSelectedEntry(selectedResultIndex + 1);
    }
    
    function searchResultsUp() {
        if (searchResults.length < 2) {
            return; // Nothing to change for 0 or 1 results
        }
        if (selectedResultIndex === 0) {
            return; // Can't go up from the first result
        }
        setSelectedEntry(selectedResultIndex - 1);
    }
    
    function setSelectedEntry(index) {
        if (selectedResultIndex < searchResults.length) {
            searchResults[selectedResultIndex].element.classList.remove("keyboard-selected");
        }
        if (index < searchResults.length) {
            searchResults[index].element.classList.add("keyboard-selected");
        }
        selectedResultIndex = index;
    }
    
    function toggleSearchBusFilter() {
        searchIncludeBuses = !searchIncludeBuses;
        toggleFilter(searchIncludeBuses, "search-filter-bus");
    }
    
    function toggleSearchRouteFilter() {
        searchIncludeRoutes = !searchIncludeRoutes;
        toggleFilter(searchIncludeRoutes, "search-filter-route");
    }
    
    function toggleSearchStopFilter() {
        searchIncludeStops = !searchIncludeStops;
        toggleFilter(searchIncludeStops, "search-filter-stop");
    }
    
    function toggleSearchBlockFilter() {
        searchIncludeBlocks = !searchIncludeBlocks;
        toggleFilter(searchIncludeBlocks, "search-filter-block");
    }
    
    function toggleFilter(selected, id) {
        const element = document.getElementById(id);
        if (selected) {
            element.classList.remove("inactive");
        } else {
            element.classList.add("inactive");
        }
        searchPage = 0;
        search();
    }
    
    function searchInputChanged() {
        searchPage = 0;
        search();
    }
    
    function searchNextPage() {
        searchPage += 1;
        search();
    }
    
    function searchPreviousPage() {
        if (searchPage === 0) {
            return;
        }
        searchPage -= 1;
        search();
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
        if ("map" in window) {
            map.updateSize();
        }
    }
</script>
