<div id="loading-container" class="display-none">
    <div id="loading">
        <div id="loading-line"></div>
        <div id="loading-stop">
            % include('components/svg', name='stop')
        </div>
    </div>
    <h2>Loading...</h2>
    <script>
        const loadingStopElement = document.getElementById("loading-stop");
        let loadingStopPosition = -36;
        let loadingInterval = null;
        
        function moveLoadingStop() {
            if (loadingStopPosition === -36) {
                loadingStopPosition = document.getElementById("loading").offsetWidth;
            } else {
                loadingStopPosition -= 1;
            }
            loadingStopElement.style.left = loadingStopPosition + "px";
        }
        
        function startLoading() {
            stopLoading();
            document.getElementById("loading-container").classList.remove("display-none");
            loadingInterval = setInterval(moveLoadingStop, 10);
        }
        
        function stopLoading() {
            document.getElementById("loading-container").classList.add("display-none");
            if (loadingInterval !== null) {
                clearInterval(loadingInterval);
                loadingInterval = null;
            }
        }
    </script>
</div>
