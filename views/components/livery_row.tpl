
% if liveries:
    <div class="row gap-5 livery-row">
        % for livery in liveries:
            <img class="livery" src="/img/liveries/{{ livery.id }}.png" onclick="setLiveryTheme('{{ livery.id }}')" />
        % end
    </div>
% end
