
% page = get('page', 1)
% items_per_page = get('items_per_page', 100)
% total_items = get('total_items', 0)

% max_pages = -(-total_items // items_per_page)

% if max_pages > 1 and 1 <= page <= max_pages:
    % page_numbers = {1, page, max_pages}
    % for i in range(1, 6):
        % lower = page - i
        % if 1 < lower < max_pages:
            % page_numbers.add(lower)
        % end
        % higher = page + i
        % if 1 < higher < max_pages:
            % page_numbers.add(higher)
        % end
        % if len(page_numbers) >= 7:
            % break
        % end
    % end
    <div class="paging">
        % previous_page = 0
        % for page_number in sorted(page_numbers):
            % if page_number > previous_page + 1:
                <div class="lighter-text flex-1 centred">...</div>
            % end
            % if page_number == page:
                <div class="page current flex-1">{{ page_number }}</div>
            % else:
                <a class="page flex-1" href="?page={{ page_number }}">{{ page_number }}</a>
            % end
            % previous_page = page_number
        % end
    </div>
% end
