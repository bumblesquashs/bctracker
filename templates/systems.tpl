% rebase('base', title='Change System')

<h1>Change System</h1>
<h2>Currently Viewing {{ system }}</h2>
<hr />

<table class="pure-table pure-table-horizontal pure-table-striped">
  <thead>
    <tr>
      <th>System</th>
    </tr>
  </thead>
  <tbody>
    % for available_system in sorted(systems):
      % if system != available_system:
        <tr>
          <td><a href="{{ get_url(available_system.id) }}">{{ available_system }}</a></td>
        </tr>
      % end
    % end
  </tbody>
</table>
