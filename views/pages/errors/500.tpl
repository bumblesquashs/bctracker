
% rebase('base')

<div class="page-header">
    <h1 class="title">Error: 500 Internal Server Error</h1>
</div>

<div class="placeholder">
    <h3>Looks like those lazy developers need to get their act together!</h3>
    
    <div>
        Please email <a href="mailto:james@bctracker.ca">james@bctracker.ca</a> to let us know about this error so we can look into it.
    </div>
    
    <div class="button-container">
        <button class="button" onclick="window.history.back()">Back</button>
        <button class="button" onclick="document.getElementById('error-details').classList.remove('display-none')">Show Details</button>
    </div>
    
    <div id="error-details" class="flex-column left flex-gap-10 display-none">
        <h3>{{ error.exception }}</h3>
        <div class="code-block">{{ error.traceback }}</div>
    </div>
</div>
