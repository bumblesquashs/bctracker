<div id="loading">
    <div id="loading-line"></div>
    <div id="loading-stop">
        % include('components/svg', name='stop')
    </div>
    <script>
        const loadingStopElement = document.getElementById("loading-stop");
        let loadingStopPosition = -36;
        
        function moveLoadingStop() {
            if (loadingStopPosition === -36) {
                loadingStopPosition = document.getElementById("loading").offsetWidth;
            } else {
                loadingStopPosition -= 1;
            }
            loadingStopElement.style.left = loadingStopPosition + "px";
        }
        
        const loadingInterval = setInterval(moveLoadingStop, 10);
        
        function stopLoadingInterval() {
            clearInterval(loadingInterval);
        }
    </script>
</div>
