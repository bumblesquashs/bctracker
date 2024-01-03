
% rebase('base')

% if system_id is None:
    <div class="page-header">
        <h1 class="title">Error: System Required</h1>
    </div>

    <div class="placeholder">
        <h3 class="title">The page you are trying to look at requires a system</h3>
        <p>Please choose a system.</p>
    </div>
% else:
    <div class="page-header">
        <h1 class="title">Error: System "{{ system_id }}" Not Found</h1>
    </div>

    <div class="placeholder">
        <h3 class="title">The system you are looking at doesn't seem to exist!</h3>
        <p>
            Somehow you managed to view an invalid system, which is difficult (though obviously not impossible) to do.
            Congratuations!
        </p>
        <p>Please choose a valid system and think about what you've done.</p>
    </div>
% end
