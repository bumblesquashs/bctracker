
<script>
    function toggleMapZ() {
        const mapElement = document.getElementById("map");
        const toggleElement = document.getElementById("map-z-toggle");
        const iconElement = document.getElementById("map-z-toggle-icon");
        mapElement.classList.toggle("z-override");
        toggleElement.classList.toggle("active");
        if (mapElement.classList.contains("z-override")) {
            iconElement.src = "/img/white/close-fullscreen.png";
        } else {
            iconElement.src = "/img/white/open-fullscreen.png";
        }
    }
</script>

<div id="map-z-toggle" class="mobile-only" onclick="toggleMapZ()">
    <img id="map-z-toggle-icon" src="/img/white/open-fullscreen.png" />
</div>
