
% rebase('base', title='Themes')

<div class="page-header">
    <h1 class="title">Themes</h1>
    % if theme is None:
        <h2 class="subtitle">Current Theme: BC Transit</h2>
    % else:
        <h2 class="subtitle">Current Theme: {{ theme }}</h2>
    % end
    <hr />
</div>

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

<div class="theme-control">
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
