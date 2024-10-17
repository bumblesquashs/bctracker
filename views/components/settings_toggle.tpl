<div class="non-desktop toggle-button" onclick="toggleSettings()">
    % include('components/svg', name='settings')
</div>
<script>
    function toggleSettings() {
        document.getElementById("{{ get('settings_element', 'settings') }}").classList.toggle("collapsed");
    }
</script>
