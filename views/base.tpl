<html>
    <head> 
        <title>
            % if system is None:
                BCTracker | {{ title }}
            % else:
                {{ system }} | {{ title }}
            % end
        </title>
        
        <link rel="icon" type="image/png" href="/img/favicon.png" />
        
        <!-- prevent this website from being searchable -->
        <meta name="robots" content="noindex" />
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        
        <link rel="stylesheet" href="/style/main.css?version={{ version }}" />
        <link rel="stylesheet" href="/style/tables.css?version={{ version }}" />
        
        <link rel="stylesheet" media="screen and (min-width: 1001px)" href="/style/desktop.css?version={{ version }}" />
        <link rel="stylesheet" media="screen and (min-width: 501px) and (max-width: 1000px)" href="/style/tablet.css?version={{ version }}" />
        <link rel="stylesheet" media="screen and (max-width: 500px)" href="/style/mobile.css?version={{ version }}" />
        
        % if theme == "light":
            <link rel="stylesheet" href="/style/light.css?version={{ version }}" />
            
            <script>
                const prefersDarkScheme = false
            </script>
        % elif theme == "dark":
            <link rel="stylesheet" href="/style/dark.css?version={{ version }}" />
            
            <script>
                const prefersDarkScheme = true
            </script>
        % elif theme == "classic":
            <link rel="stylesheet" href="/style/classic.css?version={{ version }}" />
            
            <script>
                const prefersDarkScheme = false
            </script>
        % else:
            <link rel="stylesheet" media="screen and (prefers-color-scheme: light)" href="/style/light.css?version={{ version }}" />
            <link rel="stylesheet" media="screen and (prefers-color-scheme: dark)" href="/style/dark.css?version={{ version }}" />
            
            <script>
                const prefersDarkScheme = window.matchMedia("screen and (prefers-color-scheme: dark)").matches;
            </script>
        % end
        
        % if defined("include_maps") and include_maps:
            <script src='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.js'></script>
            <link href='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.css' rel='stylesheet' />
            
            <script>
                mapboxgl.accessToken = '{{mapbox_api_key}}';
            </script>
        % end
        
        <script>
            function toggleMenu() {
                document.getElementById("menu").classList.toggle("display-none");
                document.getElementById("search-non-desktop").classList.add("display-none");
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
                document.getElementById("menu").classList.add("display-none");
            }
            
            function searchNonDesktop() {
                const inputElement = document.getElementById("search-non-desktop-input");
                const resultsElement = document.getElementById("search-non-desktop-results");
                search(inputElement, resultsElement);
            }
            
            function search(inputElement, resultsElement) {
                const query = inputElement.value;
                if (query === undefined || query === null || query === "") {
                    resultsElement.classList.add("display-none");
                    resultsElement.innerHTML = "";
                    inputElement.onkeyup = function() {};
                } else {
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
                            if (count === 1) {
                                inputElement.onkeyup = function(event) {
                                    if (event.keyCode === 13) {
                                        event.preventDefault();
                                        window.location = results[0].url;
                                    }
                                };
                            } else {
                                inputElement.onkeyup = function() {};
                            }
                        }
                    };
                    request.onerror = function() {
                        resultsElement.innerHTML = "<div class='message'>Error loading search results</div>";
                        inputElement.onkeyup = function() {};
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
                for (const result of results) {
                    let name = result.name;
                    switch (result.type) {
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
                        <a href='" + result.url + "'>" +
                            name +
                            "<br />\
                            <span class='smaller-font lighter-text'>" + result.description + "</span>\
                        </a>";
                }
                return html;
            }
            
            function openSurvey() {
                window.open("https://docs.google.com/forms/d/e/1FAIpQLSfxtrvodzaJzmNwt6CQxfDfQcR2F9D6crOrxwCtP6LA6aeCgQ/viewform?usp=sf_link", "_blank").focus();
                hideSurvey();
            }
            
            function hideSurvey() {
                document.getElementById("survey-banner").classList.add("display-none");
                const now = new Date();
                const expireTime = now.getTime() + 1000 * 60 * 60 * 24 * 60;
                now.setTime(expireTime);
                
                document.cookie = "survey_banner=hide;expires=" + now.toUTCString() + ";domain={{ '' if cookie_domain is None else cookie_domain }};path=/";
            }
        </script>
    </head>
    
    <body>
        <div id="header">
            <a class="header-button title" href="{{ get_url(system) }}">BCTracker</a>
            
            <div class="desktop-only">
                % if system is None or system.realtime_enabled:
                    <a class="header-button" href="{{ get_url(system, 'map') }}">Map</a>
                    <a class="header-button" href="{{ get_url(system, 'realtime') }}">Realtime</a>
                    <a class="header-button" href="{{ get_url(system, 'history') }}">History</a>
                % else:
                    <span class="header-button disabled">Map</span>
                    <span class="header-button disabled">Realtime</span>
                    <span class="header-button disabled">History</span>
                % end
                
                <a class="header-button" href="{{ get_url(system, 'routes') }}">Routes</a>
                <a class="header-button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
                <a class="header-button" href="{{ get_url(system, 'about') }}">About</a>
                
                % if len(systems) > 1:
                    % path = get('path', '')
                    <div class="header-button dropdown right" id="system-dropdown">
                        Change System
                        <div class="content">
                            % if system is None:
                                <a class="disabled">All Systems</a>
                            % else:
                                <a href="{{ get_url(None, path) }}">All Systems</a>
                            % end
                            % sorted_systems = sorted(systems)
                            <table>
                                <tbody>
                                    % for i in range(0, len(sorted_systems), 2):
                                        <tr>
                                            % left_system = sorted_systems[i]
                                            <td>
                                                % if system is not None and system == left_system:
                                                    <a class="disabled">{{ left_system }}</a>
                                                % else:
                                                    <a href="{{ get_url(left_system, path) }}">{{ left_system }}</a>
                                                % end
                                            </td>
                                            % if i < len(sorted_systems) - 1:
                                                % right_system = sorted_systems[i + 1]
                                                <td>
                                                    % if system is not None and system == right_system:
                                                        <a class="disabled">{{ right_system }}</a>
                                                    % else:
                                                        <a href="{{ get_url(right_system, path) }}">{{ right_system }}</a>
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
                
                <div id="search-desktop" class="header-text right">
                    <img src="/img/search.png" />
                    <input type="text" id="search-desktop-input" placeholder="Search" oninput="searchDesktop()" onfocus="searchDesktopFocus()" onblur="searchDesktopBlur()">
                    
                    <div id="search-desktop-results" class="display-none"></div>
                </div>
            </div>
            
            <div class="tablet-only">
                % if system is None or system.realtime_enabled:
                    <a class="header-button" href="{{ get_url(system, 'map') }}">Map</a>
                    <a class="header-button" href="{{ get_url(system, 'realtime') }}">Realtime</a>
                % else:
                    <a class="header-button" href="{{ get_url(system, 'routes') }}">Routes</a>
                    <a class="header-button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
                % end
            </div>
            
            <div class="menu-toggle non-desktop right" onclick="toggleMenu()">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
            </div>
            
            <div class="search-non-desktop-toggle non-desktop right" onclick="toggleSearchNonDesktop()">
                <img src="/img/search.png" />
            </div>
            
            <br style="clear: both" />
        </div>
        
        <div id="menu" class="non-desktop display-none">
            <div class="tablet-only">
                % if system is None or system.realtime_enabled:
                    <a class="header-button" href="{{ get_url(system, 'history') }}">History</a>
                    <a class="header-button" href="{{ get_url(system, 'routes') }}">Routes</a>
                    <a class="header-button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
                % end
            </div>
            
            <div class="mobile-only">
                % if system is None or system.realtime_enabled:
                    <a class="header-button" href="{{ get_url(system, 'map') }}">Map</a>
                    <a class="header-button" href="{{ get_url(system, 'realtime') }}">Realtime</a>
                    <a class="header-button" href="{{ get_url(system, 'history') }}">History</a>
                % end
                <a class="header-button" href="{{ get_url(system, 'routes') }}">Routes</a>
                <a class="header-button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
            </div>
            
            <a class="header-button" href="{{ get_url(system, 'about') }}">About</a>
            
            % if len(systems) > 1:
                % path = get('path', '')
                <a class="header-button" href="{{ get_url(system, f'systems?path={path}') }}">Change System</a>
            % end
        </div>
        
        <div id="search-non-desktop" class="non-desktop display-none">
            <input type="text" id="search-non-desktop-input" placeholder="Search" oninput="searchNonDesktop()">
            
            <div id="search-non-desktop-results" class="display-none"></div>
        </div>
        
        <div id="subheader">
            <div id="system">
                % if system is None:
                    All Transit Systems
                % elif system.id == 'fvx':
                    Fraser Valley Express
                % else:
                    {{ system }} Regional Transit System
                % end
            </div>
            % if system is None or system.realtime_enabled:
                <div id="last-updated">Updated {{ last_updated }}</div>
            % end
        </div>
        
        % if show_survey_banner:
            <div id="survey-banner">
                <span class="close-button" onclick="hideSurvey()"><img width="24px" height="24px" src="/img/close.png"/></span>
                <div class="content">
                    <span class="title">Take the BCTracker Survey!</span>
                    <br />
                    <span class="description">For more information, check out the latest update on the <a href="{{ get_url(system) }}">home page</a></span>
                </div>
                <button class="button survey-button" onclick="openSurvey()">Start Now</button>
            </div>
        % end
        
        <div id="content">{{ !base }}</div>
    </body>
</html>
