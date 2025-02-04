
<script>
    function toggleMap() {
        document.getElementById("open-map-toggle-icon").classList.toggle('display-none');
        document.getElementById("close-map-toggle-icon").classList.toggle('display-none');
        document.getElementById("navigation-bar").classList.toggle("display-none");
        document.getElementById("navigation-menu").classList.add("display-none");
        document.getElementById("search").classList.add("display-none");
        document.getElementById("side-bar").classList.toggle("display-none");
        document.getElementById("banners").classList.toggle("display-none");
        document.getElementById("page").classList.toggle("display-none");
        map.updateSize();
    }
</script>

<div id="map-toggle" class="mobile-only" onclick="toggleMap()">
    <div id="open-map-toggle-icon">
        % include('components/svg', name='fullscreen-open')
    </div>
    <div id="close-map-toggle-icon" class="display-none">
        % include('components/svg', name='fullscreen-close')
    </div>
</div>
