
% rebase('base')

<div id="page-header">
    <h1>News Archive</h1>
    <a href="{{ context.url() }}">Return home</a>
</div>

% if news_views:
    <div class="container">
        % for news_view in news_views:
            % include(news_view)
        % end
    </div>
    % include('components/top_button')
% else:
    <div class="placeholder">
        <h3>No news yet</h3>
        <p>Please check back later!</p>
    </div>
% end
