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
        
        <link rel="stylesheet" href="/style/main.css" />
        <link rel="stylesheet" media="screen and (min-width: 803px)" href="/style/desktop.css" />
        <link rel="stylesheet" media="screen and (max-width: 802px)" href="/style/mobile.css" />
        <link rel="stylesheet" href="/style/tables.css" />
        
        % if defined("include_maps") and include_maps:
            <script src='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.js'></script>
            <link href='https://api.mapbox.com/mapbox-gl-js/v1.11.1/mapbox-gl.css' rel='stylesheet' />
            
            <script>
                mapboxgl.accessToken = '{{mapbox_api_key}}';
            </script>
        % end
        
        <script>
            function toggleMobileHeader() {
                document.getElementById("mobile-header").classList.toggle("display-none")
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
                    <div class="header-button dropdown" id="system-dropdown">
                        Change System
                        <div class="content">
                            % if system is None:
                                <a class="disabled">All Systems</a>
                            % else:
                                <a href="{{ get_url(None, get('path', '')) }}">All Systems</a>
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
                                                    <a href="{{ get_url(left_system, get('path', '')) }}">{{ left_system }}</a>
                                                % end
                                            </td>
                                            % if i < len(sorted_systems) - 1:
                                                % right_system = sorted_systems[i + 1]
                                                <td>
                                                    % if system is not None and system == right_system:
                                                        <a class="disabled">{{ right_system }}</a>
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
            
            <div class="mobile-toggle mobile-only" onclick="toggleMobileHeader()">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
            </div>
            
            <br style="clear: both" />
        </div>
        
        <div id="mobile-header" class="mobile-only display-none">
            % if system is None or system.realtime_enabled:
                <a class="header-button" href="{{ get_url(system, 'map') }}">Map</a>
                <a class="header-button" href="{{ get_url(system, 'realtime') }}">Realtime</a>
                <a class="header-button" href="{{ get_url(system, 'history') }}">History</a>
            % end
            <a class="header-button" href="{{ get_url(system, 'routes') }}">Routes</a>
            <a class="header-button" href="{{ get_url(system, 'blocks') }}">Blocks</a>
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
        
        <div id="content">{{ !base }}</div>
    </body>
</html>
