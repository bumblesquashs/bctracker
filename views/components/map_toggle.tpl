
<script>
    function toggleMap() {
        const headerElement = document.getElementById("header");
        const sideBarElement = document.getElementById("side-bar");
        const bannersElement = document.getElementById("banners");
        const mapElement = document.getElementById("map");
        const toggleElement = document.getElementById("map-toggle");
        const whiteIconElement = document.getElementById("map-toggle-icon-white");
        const blackIconElement = document.getElementById("map-toggle-icon-black");
        headerElement.classList.toggle("display-none");
        sideBarElement.classList.toggle("display-none");
        bannersElement.classList.toggle("display-none");
        mapElement.classList.toggle("z-override");
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
