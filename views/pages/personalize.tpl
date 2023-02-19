
% rebase('base', title='Personalize', enable_refresh=False)

<div class="page-header">
    <h1 class="title">Personalize</h1>
    <hr />
</div>
<div class="flex-container">
    <div class="container flex-1">
        <div class="section">
            <div class="header">
                <h2>Theme</h2>
                % if theme is None:
                    <h3>Current Theme: BC Transit</h3>
                % else:
                    <h3>Current Theme: {{ theme }}</h3>
                % end
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
                
                <div class="button-container">
                    <a class="button" href="?theme=automatic">BC Transit (Auto)</a>
                    % for visible_theme in visible_themes:
                        <a class="button" href="?theme={{ visible_theme.id }}">{{ visible_theme }}</a>
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
                % if time_format is None:
                    <h3>Current Format: 24hr</h3>
                % else:
                    <h3>Current Format: {{ time_format }}</h3>
                % end
            </div>
            <div class="content">
                <p>
                    You can choose whether times are displayed as 12hr or 24hr.
                </p>
                <p>
                    Since buses running between midnight and early morning are considered part of the previous day's schedule, both formats modify how those times are shown.
                    The 12hr format uses xm instead of am, so 1am is shown as 1xm.
                    The 24hr format continues increasing the hour, so 1am is shown as 25:00.
                </p>
                <div class="button-container">
                    <a class="button" href="?time_format=12hr">12hr</a>
                    <a class="button" href="?time_format=24hr">24hr</a>
                </div>
            </div>
        </div>
    </div>
</div>
