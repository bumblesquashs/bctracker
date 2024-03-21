
% if block:
    <a href="{{ get_url(block.system, f'blocks/{block.id}') }}">{{ block.id }}</a>
% else:
    <span class="lighter-text">Unavailable</span>
% end
