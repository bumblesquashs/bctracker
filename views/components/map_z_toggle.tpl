
<script>
    function toggleMapZ() {
        const mapElement = document.getElementById("map");
        const toggleElement = document.getElementById("map-z-toggle");
        const whiteIconElement = document.getElementById("map-z-toggle-icon-white");
        const blackIconElement = document.getElementById("map-z-toggle-icon-black");
        mapElement.classList.toggle("z-override");
        toggleElement.classList.toggle("active");
        if (mapElement.classList.contains("z-override")) {
            whiteIconElement.src = "/img/white/close-fullscreen.png";
            blackIconElement.src = "/img/black/close-fullscreen.png";
        } else {
            whiteIconElement.src = "/img/white/open-fullscreen.png";
            blackIconElement.src = "/img/black/open-fullscreen.png";
        }
    }
</script>

<div id="map-z-toggle" class="mobile-only" onclick="toggleMapZ()">
    <img id="map-z-toggle-icon-white" src="/img/white/open-fullscreen.png" />
    <img id="map-z-toggle-icon-black" src="/img/black/open-fullscreen.png" />
</div>
