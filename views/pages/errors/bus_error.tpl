
% rebase('base', title='Error')

<div class="page-header">
    <h1 class="title">Error: Bus {{ bus_number }} Not Found</h1>
    <hr />
</div>

<p>The bus you are looking for doesn't seem to exist!</p>
<p>
    There are a few reasons why that might be the case:
    <ol>
        <li>It may be the wrong number - are you sure bus {{ bus_number }} is the one you want?</li>
        <li>It may have been retired before this tracker was started</li>
        <li>It may be a brand new bus that hasn't been registered with the tracker yet</li>
    </ol>
</p>

<p>
    If you believe this error is incorrect and the bus actually should exist, please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know!
</p>

<p>
    <button class="button" onclick="window.history.back()">Back</button>
</p>
