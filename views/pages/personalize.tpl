
% rebase('base')

<div id="page-header">
    <h1>Personalize</h1>
</div>

<div class="page-container">
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>Theme</h2>
            </div>
            <div class="content">
                <p>
                    The default BCTracker theme (BC Transit) is available in both light and dark colours.
                    You can also set it to change automatically based on your system preferences.
                    Alternatively, you can embrace nostalgia with themes based on older BC transit agencies.
                </p>
                <p>
                    A high contrast option is also available to help distinguish some parts of the website better for anyone who is visually impaired.
                </p>
                
                % visible_themes = [t for t in themes if t.visible]
                % hidden_themes = [t for t in themes if not t.visible]
                
                <div class="options-container">
                    <div class="option" onclick="setTheme('automatic')">
                        <div class="radio-button {{ 'selected' if theme is None else '' }}"></div>
                        <div>BC Transit (Auto)</div>
                    </div>
                    
                    % for visible_theme in visible_themes:
                        <div class="option" onclick="setTheme('{{ visible_theme.id }}')">
                            <div class="radio-button {{ 'selected' if theme is not None and visible_theme == theme else '' }}"></div>
                            <div>{{ visible_theme }}</div>
                        </div>
                    % end
                    
                    % if theme is not None and not theme.visible:
                        <div class="option" onclick="setTheme('{{ theme.id }}')">
                            <div class="radio-button selected"></div>
                            <div>{{ theme }}</div>
                        </div>
                    % end
                </div>
                
                % if len(hidden_themes) > 0:
                    <!-- Well well well... are you really so desperate for new themes that you'll willing to dig into the source code to find more? -->
                    <!-- I suppose you'll have to be rewarded for your efforts. Here's a list of secret themes that are available: -->
                    % for hidden_theme in hidden_themes:
                        <!-- {{ hidden_theme.id }} ({{ hidden_theme }}) -->
                    % end
                    <!-- More secret themes may be added in the future, if you ever feel the need to look at this list again someday. -->
                    <!-- If you aren't sure how to actually apply secret themes, I'm afraid you'll just have to figure it out yourself. -->
                    <!-- I was generous to even give you this list in the first place! ;) -->
                % end
            </div>
        </div>
    </div>
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>Time Format</h2>
            </div>
            <div class="content">
                <p>You can choose whether times are displayed as 12hr or 30hr.</p>
                <p>Since buses running between midnight and early morning are considered part of the previous day's schedule, both formats modify how those times are shown.</p>
                <div class="options-container">
                    <div class="option" onclick="setTimeFormat('12hr')">
                        <div class="radio-button {{ 'selected' if time_format == '12hr' else '' }}"></div>
                        <div class="column">
                            <p>12hr</p>
                            <p class="smaller-font lighter-text">Uses xm instead of am, so 1am is shown as 1xm</p>
                        </div>
                    </div>
                    <div class="option" onclick="setTimeFormat('30hr')">
                        <div class="radio-button {{ 'selected' if time_format is None or time_format == '24hr' or time_format == '30hr' else '' }}"></div>
                        <div class="column">
                            <p>30hr</p>
                            <p class="smaller-font lighter-text">Continues increasing the hour beyond a normal 24 hour clock, so 1am is shown as 25:00</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>Map Bus Icon Style</h2>
            </div>
            <div class="content">
                <p>Choose a style for bus icons shown on the map screen.</p>
                <div class="options-container">
                    <div class="option" onclick="setBusMarkerStyle('default')">
                        <div class="radio-button {{ 'selected' if bus_marker_style is None or bus_marker_style == 'default' else '' }}"></div>
                        <div>Default</div>
                    </div>
                    <div class="option" onclick="setBusMarkerStyle('mini')">
                        <div class="radio-button {{ 'selected' if bus_marker_style == 'mini' else '' }}"></div>
                        <div>Mini</div>
                    </div>
                    <div class="option" onclick="setBusMarkerStyle('adherence')">
                        <div class="radio-button {{ 'selected' if bus_marker_style == 'adherence' else '' }}"></div>
                        <div>Schedule Adherence</div>
                    </div>
                    <div class="option" onclick="setBusMarkerStyle('route')">
                        <div class="radio-button {{ 'selected' if bus_marker_style == 'route' else '' }}"></div>
                        <div>Route Number</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    function setTheme(themeID) {
        window.location = "?theme=" + themeID
    }
    
    function setTimeFormat(format) {
        window.location = "?time_format=" + format
    }
    
    function setBusMarkerStyle(style) {
        window.location = "?bus_marker_style=" + style
    }
</script>
