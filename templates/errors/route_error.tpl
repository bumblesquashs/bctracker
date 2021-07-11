% rebase('base', title='Error')

<h1>Error: Route {{ number }} Not Found</h1>
<hr />

<p>The route you are looking for doesn't seem to exist!</p>
<p>
  There are a few reasons why that might be the case:
  <ol>
    <li>It may be from an older service sheet that is no longer used</li>
    <li>It may be the wrong number - are you sure route {{ number }} is the one you want?</li>
    % if system is not None:
      <li>It may be from a different system - you're currently looking at {{ system }}</li>
    % end
  </ol>
</p>

<p>
  If you believe this error is incorrect and the route actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!
</p>

<p>
  <button class="button" onclick="window.history.back()">Back</button>
</p>