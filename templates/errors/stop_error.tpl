% rebase('base', title='Error')

<h1>Error: Stop {{ number }} Not Found</h1>
<hr />

<p>The stop you are looking for doesn't seem to exist!</p>
<p>
  There are a few reasons why that might be the case:
  <ol>
    <li>It may no longer serve any bus routes and therefore be removed from the system</li>
    <li>It may be the wrong number - are you sure stop {{ number }} is the one you want?</li>
    % if system is not None:
      <li>It may be from a different system - you're currently looking at {{ system }}</li>
    % end
  </ol>
</p>

<p>
  If you believe this error is incorrect and the stop actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!
</p>

<p>
  <button class="button" onclick="window.history.back()">Back</button>
</p>
