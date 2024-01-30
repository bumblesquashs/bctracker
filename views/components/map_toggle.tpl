
<script>
    function toggleMap() {
        const toggleElement = document.getElementById("map-toggle");
        const whiteIconElement = document.getElementById("map-toggle-icon-white");
        const blackIconElement = document.getElementById("map-toggle-icon-black");
        document.getElementById("navigation-bar").classList.toggle("display-none");
        document.getElementById("navigation-menu").classList.add("display-none");
        document.getElementById("search").classList.add("display-none");
        document.getElementById("side-bar").classList.toggle("display-none");
        document.getElementById("banners").classList.toggle("display-none");
        document.getElementById("map").classList.toggle("z-override");
        toggleElement.classList.toggle("active");
        if (toggleElement.classList.contains("active")) {
            whiteIconElement.src = "/img/white/close-fullscreen.png";
            blackIconElement.src = "/img/black/close-fullscreen.png";
        } else {
            whiteIconElement.src = "/img/white/open-fullscreen.png";
            blackIconElement.src = "/img/black/open-fullscreen.png";
        }
        map.resize();
    }
</script>

<div id="map-toggle" class="mobile-only" onclick="toggleMap()">
    <img id="map-toggle-icon-white" src="/img/white/open-fullscreen.png" />
    <img id="map-toggle-icon-black" src="/img/black/open-fullscreen.png" />
</div>
