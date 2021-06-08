% include('components/header', title='Invalid System')

<h1>Error: Invalid System ({{ system_id }})</h1>

<script>
    function back() {
        window.history.back()
    }
</script>
<button class="button" onclick="back()">Back</button>

% include('components/footer')
