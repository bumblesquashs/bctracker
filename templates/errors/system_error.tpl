% rebase('base', title='Error')

% if system_id is None:
  <h1>Error: System Required</h1>
  <hr />

  <p>The page you are trying to look at requires a system.</p>
  <p>Please choose a system.</p>
% else:
  <h1>Error: System {{ system_id }} Not Found</h1>
  <hr />

  <p>The system you are looking at doesn't seem to exist!</p>
  <p>
    Somehow you managed to view an invalid system, which is difficult (though obviously not impossible) to do.
    Congratuations!
  </p>
  <p>Please choose a valid system and think about what you've done.</p>
% end

% include('components/systems')