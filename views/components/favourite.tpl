
% from models.favourite import Favourite

% if type == 'vehicle':
    % favourite = Favourite(bus.order.agency.id, 'vehicle', str(bus.number))
% elif type == 'route':
    % favourite = Favourite(route.system.id, 'route', route.number)
% elif type == 'stop':
    % favourite = Favourite(stop.system.id, 'stop', stop.number)
% else:
    % favourite = None
% end

% if favourite in favourites:
    <div class="favourite tooltip-anchor" onclick="removeFavourite()">
        % include('components/svg', name='favourite')
        <div class="tooltip right">Remove favourite</div>
    </div>
    <script>
        function removeFavourite() {
            setCookie("favourites", "{{ favourites.removing(favourite) }}");
            location.reload();
        }
    </script>
% else:
    % if favourites.is_full:
        <div class="favourite disabled tooltip-anchor">
            % include('components/svg', name='non-favourite')
            <div class="tooltip right">Too many favourites</div>
        </div>
    % else:
        <div class="favourite tooltip-anchor" onclick="addFavourite()">
            % include('components/svg', name='non-favourite')
            <div class="tooltip right">Add favourite</div>
        </div>
        <script>
            function addFavourite() {
                setCookie("favourites", "{{ favourites.adding(favourite) }}");
                location.reload();
            }
        </script>
    % end
% end
