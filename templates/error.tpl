% rebase('base', title='Error')

<h1>Error: {{ error }}</h1>
% if defined('message') and message is not None:
  <h2>{{ message }}</h2>
% end
<hr />

<script>
  function back() {
    window.history.back()
  }
</script>
<button class="button" onclick="back()">Back</button>
