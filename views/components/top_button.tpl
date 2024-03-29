<div id="top-button" class="button" onclick="scrollToTop()">Back to Top</div>

<script>
    const topButton = document.getElementById("top-button");
    const contentElement = document.getElementById("main");
    const height = window.innerHeight * 1.5;
    
    contentElement.onscroll = function() {
        if (contentElement.scrollTop > height) {
            topButton.style.display = "block";
        } else {
            topButton.style.display = "none";
        }
    }
    
    document.body.onscroll = function() {
        if (document.body.scrollTop > height) {
            topButton.style.display = "block";
        } else {
            topButton.style.display = "none";
        }
    }
    
    function scrollToTop() {
        contentElement.scrollTop = 0;
        document.body.scrollTop = 0;
    }
</script>

<style>
    #main {
        padding-bottom: 60px;
    }
</style>
