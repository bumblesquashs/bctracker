
<div class="button" id="top-button" onclick="scrollToTop()">Back to Top</div>

<script>
    const topButton = document.getElementById("top-button");
    const height = window.innerHeight * 1.5;
    
    window.onscroll = function() {
        if (document.body.scrollTop > height || document.documentElement.scrollTop > height) {
            topButton.style.display = "block";
        } else {
            topButton.style.display = "none";
        }
    }
    
    function scrollToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
</script>

<style>
    #content {
        padding-bottom: 60px;
    }
</style>
