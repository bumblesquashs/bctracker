
<div id="section-navigation">
    <div id="top-button" class="section-navigation-button tooltip-anchor" onclick="scrollToTop()">
        % include('components/svg', name='paging/up-double')
        <div class="tooltip left">Top of page</div>
    </div>
    <div id="previous-section-button" class="section-navigation-button tooltip-anchor" onclick="scrollToPreviousSection()">
        % include('components/svg', name='paging/up')
        <div class="tooltip left">Previous section</div>
    </div>
    <div id="next-section-button" class="section-navigation-button tooltip-anchor" onclick="scrollToNextSection()">
        % include('components/svg', name='paging/down')
        <div class="tooltip left">Next section</div>
    </div>
    <div id="bottom-button" class="section-navigation-button tooltip-anchor" onclick="scrollToBottom()">
        % include('components/svg', name='paging/down-double')
        <div class="tooltip left">Bottom of page</div>
    </div>
    
    <script>
        function evaluateAnchors() {
            const elements = document.querySelectorAll("div.container > div.section");
            if (elements.length < 2) {
                document.getElementById("previous-section-button").classList.add("display-none");
                document.getElementById("next-section-button").classList.add("display-none");
            }
        }
        
        function scrollToTop() {
            const element = document.getElementById("main");
            element.scrollTop = 0;
            document.body.scrollTop = 0;
        }
        
        function scrollToPreviousSection() {
            const elements = document.querySelectorAll("div.container > div.section");
            const validElements = [];
            for (const element of elements) {
                const rect = element.getBoundingClientRect();
                if (rect.top < 0) {
                    validElements.push(element);
                } else {
                    break;
                }
            }
            if (validElements.length === 0) {
                return;
            }
            const element = validElements[validElements.length - 1];
            element.scrollIntoView();
        }
        
        function scrollToNextSection() {
            const elements = document.querySelectorAll("div.container > div.section");
            const validElements = [];
            for (const element of elements) {
                const rect = element.getBoundingClientRect();
                if (rect.top > (window.innerHeight / 4)) {
                    validElements.push(element);
                    break;
                }
            }
            if (validElements.length === 0) {
                return;
            }
            const element = validElements[validElements.length - 1];
            element.scrollIntoView();
        }
        
        function scrollToBottom() {
            const element = document.getElementById("main");
            element.scrollTop = element.scrollHeight;
            document.body.scrollTop = document.body.scrollHeight;
        }
        
        evaluateAnchors();
    </script>
    
    <style>
        @media screen and (min-width: 1201px) {
            #main {
                padding-right: 40px;
            }
        }
        
        @media screen and (max-width: 1200px) {
            #main {
                padding-bottom: 80px;
            }
        }
    </style>
</div>
