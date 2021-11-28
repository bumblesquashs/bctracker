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
                document.getElementById("menu").classList.toggle("display-none")
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
                    <div class="header-button dropdown" id="system-dropdown">
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
            
            <div class="menu-toggle non-desktop" onclick="toggleMenu()">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
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
