
% from models.context import Context

<html>
    <head>
        % if settings.enable_analytics:
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id={{ settings.analytics_key }}"></script>
            <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag("js", new Date());
                gtag("config", "{{ settings.analytics_key }}");
            </script>
        % end
        
        <title>
            % if context.system:
                {{ context }} | {{ title }}
            % else:
                BCTracker | {{ title }}
            % end
        </title>
        
        <link rel="icon" type="image/png" href="/img/bctracker/favicon-16.png" sizes="16x16" />
        <link rel="icon" type="image/png" href="/img/bctracker/favicon-32.png" sizes="32x32" />
        <link rel="icon" type="image/png" href="/img/bctracker/favicon-48.png" sizes="48x48" />
        
        % if context.system:
            <meta name="description" content="{{ context }} Transit Schedules and {{ context.vehicle_type }} Tracking" />
            <meta name="keywords" content="Transit, British Columbia, {{ context.vehicle_type }} Tracking, {{ context }}, {{ context.agency }}" />
        % else:
            <meta name="description" content="Transit Schedules and Bus Tracking in BC" />
            <meta name="keywords" content="Transit, British Columbia, Bus Tracking" />
        % end
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta charset="UTF-8" />
        
        <meta name="format-detection" content="telephone=no">
        <meta name="format-detection" content="date=no">
        <meta name="format-detection" content="address=no">
        <meta name="format-detection" content="email=no">
        
        % if get('disable_indexing', False):
            <meta name="robots" content="noindex">
        % end
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Lora:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
        
        % if context.system:
            <meta property="og:title" content="{{ context }} | {{ title }}">
        % else:
            <meta property="og:title" content="BCTracker | {{ title }}">
        % end
        <meta property="og:description" content="Transit schedules and bus tracking" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{{ get_url(context, *path) }}" />
        <meta property="og:image" content="{{ get_url(context, 'img', 'bctracker', 'meta-logo.png') }}" />
        <meta property="og:image:type" content="image/png" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:image:alt" content="BCTracker Logo" />
        <meta property="og:site_name" content="BCTracker" />
        
        <link rel="stylesheet" href="/style/main.css?version={{ version }}" />
        
        <link rel="stylesheet" media="screen and (min-width: 1001px)" href="/style/devices/desktop.css?version={{ version }}" />
        <link rel="stylesheet" media="screen and (min-width: 501px) and (max-width: 1000px)" href="/style/devices/tablet.css?version={{ version }}" />
        <link rel="stylesheet" media="screen and (max-width: 500px)" href="/style/devices/mobile.css?version={{ version }}" />
        
        % if theme.light and theme.dark:
            % if theme_variant == 'light':
                <link rel="stylesheet" href="/style/light.css?version={{ version }}" />
                <link rel="stylesheet" href="/style/themes/{{ theme.id }}.light.css?version={{ version }}" />
                % if high_contrast:
                    <link rel="stylesheet" href="/style/contrast/light.css?version={{ version }}" />
                % end
            % elif theme_variant == 'dark':
                <link rel="stylesheet" href="/style/dark.css?version={{ version }}" />
                <link rel="stylesheet" href="/style/themes/{{ theme.id }}.dark.css?version={{ version }}" />
                % if high_contrast:
                    <link rel="stylesheet" href="/style/contrast/dark.css?version={{ version }}" />
                % end
            % else:
                <link rel="stylesheet" media="screen and (prefers-color-scheme: light)" href="/style/light.css?version={{ version }}" />
                <link rel="stylesheet" media="screen and (prefers-color-scheme: dark)" href="/style/dark.css?version={{ version }}" />
                <link rel="stylesheet" media="screen and (prefers-color-scheme: light)" href="/style/themes/{{ theme.id }}.light.css?version={{ version }}" />
                <link rel="stylesheet" media="screen and (prefers-color-scheme: dark)" href="/style/themes/{{ theme.id }}.dark.css?version={{ version }}" />
                % if high_contrast:
                    <link rel="stylesheet" media="screen and (prefers-color-scheme: light)" href="/style/contrast/light.css?version={{ version }}" />
                    <link rel="stylesheet" media="screen and (prefers-color-scheme: dark)" href="/style/contrast/dark.css?version={{ version }}" />
                % end
            % end
        % else:
            % if theme.light:
                <link rel="stylesheet" href="/style/light.css?version={{ version }}" />
            % elif theme.dark:
                <link rel="stylesheet" href="/style/dark.css?version={{ version }}" />
            % end
            <link rel="stylesheet" href="/style/themes/{{ theme.id }}.css?version={{ version }}" />
            % if high_contrast:
                % if theme.light:
                    <link rel="stylesheet" href="/style/contrast/light.css?version={{ version }}" />
                % elif theme.dark:
                    <link rel="stylesheet" href="/style/contrast/dark.css?version={{ version }}" />
                % end
            % end
        % end
        
        % if include_maps:
            <script src="/js/area.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/ol@v8.2.0/dist/ol.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v8.2.0/ol.css">
        % end
        
        % if enable_refresh and context.realtime_enabled:
            <script>
                const date = new Date();
                const timeToNextUpdate = 60 - date.getSeconds();
                
                setTimeout(function() {
                    const element = document.getElementById("refresh-button")
                    element.classList.remove("disabled");
                    element.innerHTML += "<div class='tooltip right'>Refresh Page</div>";
                    element.onclick = refresh
                }, 1000 * (timeToNextUpdate + 15));
                
                function refresh() {
                    location.reload();
                }
            </script>
        % end
        
        <script>
            const svgs = {};
            let currentSystemID;        
            
            function getSVG(name) {
                return svgs[name];
            }
            
            const showStopNumbers = "{{ context.show_stop_number }}" == "True";
        </script>
        
        % if context.system:
            <script>
                currentSystemID = "{{ context.system_id }}";
            </script>
        % else:
            <script>
                currentSystemID = null;
            </script>
        % end
        
        % include('components/svg_script', name='bus')
        % include('components/svg_script', name='ferry')
        % include('components/svg_script', name='model/type/bus-artic')
        % include('components/svg_script', name='model/type/bus-conventional')
        % include('components/svg_script', name='model/type/bus-decker')
        % include('components/svg_script', name='model/type/bus-midibus')
        % include('components/svg_script', name='model/type/bus-shuttle')
        % include('components/svg_script', name='model/type/ferry')
        % include('components/svg_script', name='ghost')
        % include('components/svg_script', name='stop')
        % include('components/svg_script', name='route')
        % include('components/svg_script', name='block')
        
        <script>
            function toggleNavigationMenu() {
                document.getElementById("navigation-menu").classList.toggle("display-none");
                document.getElementById("search").classList.add("display-none");
            }
            
            String.prototype.format = function() {
                a = this;
                for (k in arguments) {
                    a = a.replace("{" + k + "}", arguments[k])
                }
                return a
            }
            
            function getUrl(systemID, path, forceSubdomain=false, params=null) {
                let url;
                if (systemID === null || systemID === undefined) {
                    url = "{{ settings.all_systems_domain }}".format(path);
                } else if (currentSystemID !== null || forceSubdomain) {
                    url = "{{ settings.system_domain }}".format(systemID, path);
                } else {
                    url = "{{ settings.system_domain_path }}".format(systemID, path);
                }
                const query = [];
                if (params) {
                    for (const key in params) {
                        if (params.hasOwnProperty(key) && params[key] !== undefined && params[key] !== null) {
                            query.push(key + "=" + params[key]);
                        }
                    }
                }
                if (query.length === 0) {
                    return url;
                }
                return url + "?" + query.join("&")
            }
            
            function setCookie(key, value) {
                const max_age = 60*60*24*365*10;
                if ("{{ settings.cookie_domain }}" == "None") {
                    document.cookie = key + "=" + value + "; max-age=" + max_age + "; path=/";
                } else {
                    document.cookie = key + "=" + value + "; max-age=" + max_age + "; domain={{ settings.cookie_domain }}; path=/";
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
                
                document.cookie = "survey_banner=hide;expires=" + now.toUTCString() + ";domain={{ settings.cookie_domain if settings.cookie_domain else '' }};path=/";
            }
            
            function toggleSection(header) {
                const section = header.parentElement;
                section.classList.toggle("closed");
            }
            
            function getTimestampOffset() {
                const currentLocal = new Date().getTime();
                const currentRemote = parseFloat("{{ timestamp.value }}") * 1000;
                return currentLocal - currentRemote;
            }
            
            const timestampOffset = getTimestampOffset();
            const updateTimestampFunctions = [];
            
            function getDifference(t1, t2) {
                let difference = t1 - t2;
                
                const days = Math.floor(difference / 1000 / 60 / 60 / 24);
                difference -= days * 1000* 60 * 60 * 24;
                
                const hours = Math.floor(difference / 1000 / 60 / 60);
                difference -= hours * 1000 * 60 * 60;
                
                const minutes = Math.floor(difference / 1000 / 60);
                difference -= minutes * 1000 * 60;
                
                const seconds = Math.floor(difference / 1000);
                
                let parts = []
                if (days > 0) {
                    parts.push(days + "d");
                }
                if (hours > 0) {
                    parts.push(hours + "h");
                }
                if (minutes > 0) {
                    parts.push(minutes + "m");
                }
                if (seconds > 0) {
                    parts.push(seconds + "s");
                }
                return parts.join(" ") + " ago";
            }
        </script>
    </head>
    
    <body class="{{ 'full-map' if full_map else '' }}">
        <div id="navigation-bar">
            <a id="title" href="{{ get_url(context) }}">
                % include('components/svg', name='bctracker/bctracker')
                <div>BCTracker</div>
            </a>
            
            <a class="navigation-button non-mobile" href="{{ get_url(context, 'map') }}">Map</a>
            % if context.realtime_enabled:
                <a class="navigation-button non-mobile" href="{{ get_url(context, 'realtime') }}">Realtime</a>
                <a class="navigation-button desktop-only" href="{{ get_url(context, 'history') }}">History</a>
            % else:
                <div class="navigation-button non-mobile disabled">Realtime</div>
                <div class="navigation-button desktop-only disabled">History</div>
            % end
            
            <a class="navigation-button desktop-only" href="{{ get_url(context, 'routes') }}">Routes</a>
            <a class="navigation-button desktop-only" href="{{ get_url(context, 'stops') }}">Stops</a>
            % if context.enable_blocks:
                <a class="navigation-button desktop-only" href="{{ get_url(context, 'blocks') }}">Blocks</a>
            % else:
                <div class="navigation-button desktop-only disabled">Blocks</div>
            % end
            
            <a class="navigation-button desktop-only" href="{{ get_url(context, 'about') }}">About</a>
            
            <div class="flex-1"></div>
            
            % if show_random:
                <a class="navigation-button compact desktop-only tooltip-anchor" href="{{ get_url(context, 'random') }}">
                    % include('components/svg', name='random')
                    <div class="tooltip left">
                        <div class="title">Random Page</div>
                    </div>
                </a>
            % end
            
            <a class="navigation-button compact desktop-only tooltip-anchor" href="{{ get_url(context, 'nearby') }}">
                % include('components/svg', name='nearby')
                <div class="tooltip left">
                    <div class="title">Nearby Stops</div>
                </div>
            </a>
            
            <a class="navigation-button compact desktop-only tooltip-anchor" href="{{ get_url(context, 'personalize') }}">
                % include('components/svg', name='personalize')
                <div class="tooltip left">
                    <div class="title">Personalize</div>
                </div>
            </a>
            
            <div class="navigation-button compact" onclick="toggleSearch()">
                <div>
                    % include('components/svg', name='action/search')
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
            <a class="menu-button mobile-only" href="{{ get_url(context, 'map') }}">
                % include('components/svg', name='map')
                <span>Map</span>
            </a>
            % if context.realtime_enabled:
                <a class="menu-button mobile-only" href="{{ get_url(context, 'realtime') }}">
                    % include('components/svg', name='realtime')
                    <span>Realtime</span>
                </a>
                <a class="menu-button" href="{{ get_url(context, 'history') }}">
                    % include('components/svg', name='history')
                    <span>History</span>
                </a>
            % else:
                <div class="menu-button mobile-only disabled">
                    % include('components/svg', name='realtime')
                    <span>Realtime</span>
                </div>
                <div class="menu-button disabled">
                    % include('components/svg', name='history')
                    <span>History</span>
                </div>
            % end
            <a class="menu-button" href="{{ get_url(context, 'routes') }}">
                % include('components/svg', name='route')
                <span>Routes</span>
            </a>
            <a class="menu-button" href="{{ get_url(context, 'stops') }}">
                % include('components/svg', name='stop')
                <span>Stops</span>
            </a>
            % if context.enable_blocks:
                <a class="menu-button" href="{{ get_url(context, 'blocks') }}">
                    % include('components/svg', name='block')
                    <span>Blocks</span>
                </a>
            % else:
                <div class="menu-button disabled">
                    % include('components/svg', name='block')
                    <span>Blocks</span>
                </div>
            % end
            <a class="menu-button" href="{{ get_url(context, 'about') }}">
                % include('components/svg', name='about')
                <span>About</span>
            </a>
            <a class="menu-button" href="{{ get_url(context, 'nearby') }}">
                % include('components/svg', name='nearby')
                <span>Nearby</span>
            </a>
            <a class="menu-button" href="{{ get_url(context, 'personalize') }}">
                % include('components/svg', name='personalize')
                <span>Personalize</span>
            </a>
            % if show_random:
                <a class="menu-button" href="{{ get_url(context, 'random') }}">
                    % include('components/svg', name='random')
                    <span>Random Page</span>
                </a>
            % end
        </div>
        <div id="status-bar">
            <div id="system-menu-toggle" onclick="toggleSystemMenuMobile()">
                % include('components/svg', name='system')
            </div>
            <div class="details">
                <div id="system" class="tooltip-anchor" onclick="toggleSystemMenuDesktop()">
                    % if context.system:
                        {{ context }}
                    % else:
                        All Transit Systems
                    % end
                    <div class="tooltip right">Toggle Systems List</div>
                </div>
                % if last_updated:
                    <div id="last-updated">Updated {{ last_updated.format_web(time_format) }}</div>
                % end
            </div>
            % if context.realtime_enabled:
                <div id="refresh-button" class="disabled tooltip-anchor">
                    % include('components/svg', name='action/refresh')
                </div>
            % else:
                <div id="refresh-button-placeholder">
                    <!-- Used to keep mobile details centred properly -->
                </div>
            % end
        </div>
        <div id="content">
            <div id="system-menu" class="collapse-non-desktop {{ 'collapse-desktop' if hide_systems else '' }}">
                % if context.system:
                    <a href="{{ get_url(Context(), *path, **path_args) }}" class="system-button all-systems">All Transit Systems</a>
                % else:
                    <span class="system-button current all-systems">All Transit Systems</span>
                % end
                % for region in regions:
                    % region_systems = [s for s in systems if s.region == region]
                    % if region_systems:
                        <div class="header">{{ region }}</div>
                        % for system in sorted(region_systems):
                            % if system == context.system:
                                <div class="system-button current">
                                    % include('components/agency_logo', agency=system.agency)
                                    <div>{{ system }}</div>
                                </div>
                            % else:
                                <a href="{{ get_url(system.context, *path, **path_args) }}" class="system-button">
                                    % include('components/agency_logo', agency=system.agency)
                                    <div>{{ system }}</div>
                                </a>
                            % end
                        % end
                    % end
                % end
            </div>
            <div id="main">
                <div id="banners">
                    % if context.system_id == 'cowichan-valley':
                        <div class="banner">
                            <div class="content">
                                <h1>Due to ongoing job action, service in the Cowichan Valley area is currently suspended.</h1>
                                <p>For more information and updates please visit the <a target="_blank" href="https://www.bctransit.com/cowichan-valley/news">BC Transit News Page</a>.</p>
                            </div>
                        </div>
                    % end
                </div>
                % if full_map:
                    <div id="map" class="full-screen"></div>
                    <script>
                        const map = new ol.Map({
                            target: 'map',
                            controls: ol.control.defaults.defaults({
                                zoom: false,
                                rotate: false
                            }),
                            layers: [
                                new ol.layer.Tile({
                                    source: new ol.source.OSM(),
                                    className: "ol-layer tile-layer"
                                })
                            ],
                            view: new ol.View({
                                center: [0, 0],
                                zoom: 3,
                                maxZoom: 22,
                                minZoom: 3
                            }),
                            interactions: ol.interaction.defaults.defaults().extend([
                                new ol.interaction.DblClickDragZoom()
                            ])
                        });
                        map.getViewport().style.cursor = "grab";
                        map.on('pointerdrag', function(event) {
                            map.getViewport().style.cursor = "grabbing";
                        });
                        map.on('pointerup', function(event) {
                            map.getViewport().style.cursor = "grab";
                        });
                    </script>
                    
                    % include('components/loading')
                    % include('components/map_controls')
                % end
                <div id="page">{{ !base }}</div>
            </div>
            <div id="search" class="display-none" tabindex="0">
                <div id="search-header">
                    <div id="search-bar">
                        <input type="text" id="search-input" placeholder="Search" oninput="searchInputChanged()">
                    </div>
                    % if context.system:
                        <div id="search-filters">
                            <div class="flex-1">Filters:</div>
                            % if context.realtime_enabled:
                                <div id="search-filter-vehicle" class="button tooltip-anchor" onclick="toggleSearchVehicleFilter()">
                                    % include('components/svg', name=context.filter_vehicles_image_name)
                                    <div class="tooltip left">Include {{ context.vehicle_type_plural }}</div>
                                </div>
                            % end
                            <div id="search-filter-route" class="button tooltip-anchor" onclick="toggleSearchRouteFilter()">
                                % include('components/svg', name='route')
                                <div class="tooltip left">Include Routes</div>
                            </div>
                            <div id="search-filter-stop" class="button tooltip-anchor" onclick="toggleSearchStopFilter()">
                                % include('components/svg', name='stop')
                                <div class="tooltip left">Include Stops</div>
                            </div>
                            % if context.enable_blocks:
                                <div id="search-filter-block" class="button tooltip-anchor" onclick="toggleSearchBlockFilter()">
                                    % include('components/svg', name='block')
                                    <div class="tooltip left">Include Blocks</div>
                                </div>
                            % end
                        </div>
                    % end
                </div>
                <div id="search-placeholder">{{ context.search_placeholder_text() }}</div>
                <div id="search-results" class="display-none">
                    
                </div>
                <div id="search-paging" class="display-none">
                    <div id="search-paging-previous" class="icon button" onclick="searchPreviousPage()">
                        % include('components/svg', name='paging/left')
                    </div>
                    <div id="search-count" class="flex-1">
                        
                    </div>
                    <div id="search-paging-next" class="icon button" onclick="searchNextPage()">
                        % include('components/svg', name='paging/right')
                    </div>
                </div>
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
    let lastSearchTimestamp = Date.now();
    
    let searchIncludeVehicles = true;
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
            map.updateSize();
        }
    }
    
    function search() {
        const inputElement = document.getElementById("search-input");
        const placeholderElement = document.getElementById("search-placeholder");
        const query = inputElement.value;
        
        const timestamp = Date.now();
        lastSearchTimestamp = timestamp;
        
        if (query === undefined || query === null || query === "") {
            updateSearchView([], 0, "{{ context.search_placeholder_text() }}");
        } else {
            loadingResults = true;
            if (searchResults.length === 0) {
                placeholderElement.innerHTML = "Loading...";
            }
            const request = new XMLHttpRequest();
            request.open("POST", "{{ get_url(context, 'api', 'search') }}", true);
            request.responseType = "json";
            request.onload = function() {
                if (timestamp !== lastSearchTimestamp) {
                    // Discard outdated results
                    return;
                }
                const results = request.response.results;
                const total = request.response.total;
                
                updateSearchView(results, total, total === 0 ? "No Results" : "Results");
                
                if (enterPending) {
                    enterPending = false;
                    handleResultsEnter();
                }
            };
            request.onerror = function() {
                if (timestamp !== lastSearchTimestamp) {
                    // Discard outdated results
                    return;
                }
                updateSearchView([], 0, "Error loading search results");
            };
            const data = new FormData();
            data.set("query", query);
            data.set("page", searchPage);
            data.set("count", resultsPerPage);
            data.set("include_vehicles", searchIncludeVehicles ? 1 : 0);
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
        
        const icon = document.createElement("div");
        icon.innerHTML = getSVG(result.icon);
        element.appendChild(icon);
        
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
    
    function toggleSearchVehicleFilter() {
        searchIncludeVehicles = !searchIncludeVehicles;
        toggleFilter(searchIncludeVehicles, "search-filter-vehicle");
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
    
    function toggleSystemMenuMobile() {
        document.getElementById("system-menu").classList.toggle("collapse-non-desktop");
    }
    
    function toggleSystemMenuDesktop() {
        const element = document.getElementById("system-menu");
        element.classList.toggle("collapse-desktop");
        if (element.classList.contains("collapse-desktop")) {
            setCookie("hide_systems", "yes");
        } else {
            setCookie("hide_systems", "no");
        }
        if ("map" in window) {
            map.updateSize();
        }
    }
    
    function updateAllTimestamps() {
        const currentTime = new Date().getTime();
        for (const func of updateTimestampFunctions) {
            func(currentTime);
        }
    }
    
    if (updateTimestampFunctions.length > 0) {
        updateAllTimestamps();
        setInterval(updateAllTimestamps, 1000)
    }
</script>
