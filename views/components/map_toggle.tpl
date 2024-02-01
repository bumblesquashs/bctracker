
<script>
    function toggleMap() {
        document.getElementById("open-map-toggle-icon").classList.toggle('display-none');
        document.getElementById("close-map-toggle-icon").classList.toggle('display-none');
        document.getElementById("navigation-bar").classList.toggle("display-none");
        document.getElementById("navigation-menu").classList.add("display-none");
        document.getElementById("search-non-desktop").classList.add("display-none");
        document.getElementById("side-bar").classList.toggle("display-none");
        document.getElementById("banners").classList.toggle("display-none");
        document.getElementById("page-header").classList.toggle("display-none");
        map.updateSize();
    }
</script>

<div id="map-toggle" class="mobile-only" onclick="toggleMap()">
    <div id="open-map-toggle-icon" class="display-none">
        <img class="white" src="/img/white/open-fullscreen.png" />
        <img class="black" src="/img/black/open-fullscreen.png" />
    </div>
    <div id="close-map-toggle-icon">
        <img class="white" src="/img/white/close-fullscreen.png" />
        <img class="black" src="/img/black/close-fullscreen.png" />
    </div>
</div>
