
% if favourites.is_full and favourite not in favourites:
    <div class="favourite disabled tooltip-anchor">
        % include('components/svg', name='non-favourite')
        <div class="tooltip right">You can only have 10 favourites at a time</div>
    </div>
% else:
    <div id="remove-favourite" class="favourite tooltip-anchor {{ '' if favourite in favourites else 'display-none' }}" onclick="removeFavourite()">
        % include('components/svg', name='favourite')
        <div class="tooltip right">Remove favourite</div>
    </div>
    <div id="add-favourite" class="favourite tooltip-anchor {{ 'display-none' if favourite in favourites else '' }}" onclick="addFavourite()">
        % include('components/svg', name='non-favourite')
        <div class="tooltip right">Add favourite</div>
    </div>
    <script>
        function addFavourite() {
            setCookie("favourites", "{{ favourites.adding(favourite) }}");
            document.getElementById("add-favourite").classList.add("display-none");
            document.getElementById("remove-favourite").classList.remove("display-none");
        }
        
        function removeFavourite() {
            setCookie("favourites", "{{ favourites.removing(favourite) }}");
            document.getElementById("add-favourite").classList.remove("display-none");
            document.getElementById("remove-favourite").classList.add("display-none");
        }
    </script>
% end
